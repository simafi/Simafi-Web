# -*- coding: utf-8 -*-
"""
Comando para cargar el catálogo contable desde archivo TSV.

Columnas esperadas (separadas por tabulador):
  codgrupo, csgrupo, cmayor, cscuenta, cuenta, descrip,
  cta, depreciar, sccuenta2, auxi1, auxi2,
  cuentaant1, cuentaant2, cuentaant3, cuentaant4, cuentaant5

Uso:
  python manage.py load_catalogo_contable archivo.tsv --empresa=0301
  python manage.py load_catalogo_contable archivo.tsv --empresa=0301 --dry-run
"""
import csv
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from contabilidad.models import GrupoCuenta, CuentaContable


# Mapeo codgrupo (1-7) → (nombre grupo, naturaleza)
GRUPOS_CATALOGO = {
    '1': ('Activo', 'DEUDORA'),
    '2': ('Pasivo', 'ACREEDORA'),
    '3': ('Patrimonio', 'ACREEDORA'),
    '4': ('Cuentas de Orden', 'ACREEDORA'),
    '5': ('Ingresos', 'ACREEDORA'),
    '6': ('Gastos', 'DEUDORA'),
    '7': ('Gastos Administrativos y Otros', 'DEUDORA'),
}


def normalizar_codigo(cuenta):
    """Mantiene el código tal cual (con guiones)."""
    if not cuenta:
        return ''
    return cuenta.strip()


def es_codigo_padre(codigo_hijo, codigo_candidato):
    """True si codigo_candidato es prefijo de codigo_hijo (por segmentos)."""
    if not codigo_candidato or not codigo_hijo:
        return False
    # Comparar por segmentos separados por guión
    partes_hijo = codigo_hijo.replace('-', '-').split('-')
    partes_cand = codigo_candidato.replace('-', '-').split('-')
    if len(partes_cand) >= len(partes_hijo):
        return False
    for i, p in enumerate(partes_cand):
        if i >= len(partes_hijo) or partes_hijo[i] != p:
            return False
    return True


def nivel_desde_codigo(codigo):
    """Nivel jerárquico según cantidad de segmentos (guiones + 1)."""
    if not codigo:
        return 1
    return len([x for x in codigo.split('-') if x.strip()]) or 1


class Command(BaseCommand):
    help = 'Carga el plan de cuentas (catálogo contable) desde un archivo TSV.'

    def add_arguments(self, parser):
        parser.add_argument(
            'archivo',
            type=str,
            help='Ruta al archivo TSV (codgrupo, csgrupo, cmayor, cscuenta, cuenta, descrip, ...)',
        )
        parser.add_argument(
            '--empresa',
            type=str,
            default='0301',
            help='Código de empresa/municipio (default: 0301)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Solo mostrar qué se haría, sin guardar.',
        )
        parser.add_argument(
            '--replace',
            action='store_true',
            help='Eliminar cuentas existentes de esta empresa antes de cargar (opcional).',
        )

    def handle(self, *args, **options):
        archivo = options['archivo']
        empresa = options['empresa']
        dry_run = options['dry_run']
        replace = options['replace']

        if not os.path.isfile(archivo):
            self.stderr.write(self.style.ERROR(f'No existe el archivo: {archivo}'))
            return

        self.stdout.write(f'Leyendo catálogo desde: {archivo}')
        self.stdout.write(f'Empresa: {empresa}')
        if dry_run:
            self.stdout.write(self.style.WARNING('Modo dry-run: no se guardarán cambios.'))

        # Leer filas TSV
        filas = []
        with open(archivo, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                if len(row) < 6:
                    continue
                codgrupo = (row[0] or '').strip()
                csgrupo = (row[1] or '').strip()
                cmayor = (row[2] or '').strip()
                cscuenta = (row[3] or '').strip()
                cuenta = normalizar_codigo(row[4])
                descrip = (row[5] or '').strip()
                if not cuenta or not descrip:
                    continue
                filas.append({
                    'codgrupo': codgrupo,
                    'csgrupo': csgrupo,
                    'cmayor': cmayor,
                    'cscuenta': cscuenta,
                    'cuenta': cuenta,
                    'descrip': descrip,
                })

        # Añadir filas sintéticas para códigos padre que falten
        todos_codigos = {r['cuenta'] for r in filas}
        prefijos = set()
        for c in todos_codigos:
            partes = c.split('-')
            for i in range(1, len(partes)):
                prefijos.add('-'.join(partes[:i]))
        faltantes = prefijos - todos_codigos
        for cod in sorted(faltantes, key=lambda x: (len(x.split('-')), x)):
            # Inferir codgrupo del primer segmento
            primer = (cod.split('-')[0] or '1').strip()
            codgrupo = primer[0] if primer else '1'
            filas.append({
                'codgrupo': codgrupo,
                'csgrupo': '',
                'cmayor': '',
                'cscuenta': '',
                'cuenta': cod,
                'descrip': f'Grupo {cod}',
            })
        # Ordenar por nivel y luego por código para procesar padres antes que hijos
        filas.sort(key=lambda r: (nivel_desde_codigo(r['cuenta']), r['cuenta']))

        self.stdout.write(f'Filas a procesar (incl. padres): {len(filas)}')

        if dry_run:
            for r in filas[:5]:
                self.stdout.write(f"  {r['cuenta']} -> {r['descrip'][:50]}...")
            if len(filas) > 5:
                self.stdout.write(f'  ... y {len(filas) - 5} más.')
            return

        with transaction.atomic():
            # 1) Asegurar grupos
            grupos_por_cod = {}
            for cod, (nombre, naturaleza) in GRUPOS_CATALOGO.items():
                g, created = GrupoCuenta.objects.get_or_create(
                    codigo=cod,
                    defaults={
                        'nombre': nombre,
                        'naturaleza': naturaleza,
                        'orden': int(cod) if cod.isdigit() else 0,
                    },
                )
                grupos_por_cod[cod] = g
                if created:
                    self.stdout.write(f'  Grupo creado: {cod} - {nombre}')

            if replace:
                deleted, _ = CuentaContable.objects.filter(empresa=empresa).delete()
                self.stdout.write(f'  Cuentas existentes eliminadas: {deleted}')

            # 2) Crear cuentas en orden para poder resolver padre
            mapa_codigo_a_cuenta = {}  # codigo -> instancia (misma empresa)
            total_new = 0
            for r in filas:
                codgrupo = r['codgrupo'] or '1'
                grupo = grupos_por_cod.get(codgrupo) or grupos_por_cod['1']
                _, naturaleza = GRUPOS_CATALOGO.get(codgrupo, ('Activo', 'DEUDORA'))

                codigo = r['cuenta']
                nombre = r['descrip'][:200]
                nivel = nivel_desde_codigo(codigo)

                # Buscar cuenta padre (código prefijo más largo ya procesado)
                cuenta_padre = None
                for cod_prev, inst in sorted(mapa_codigo_a_cuenta.items(), key=lambda x: -len(x[0])):
                    if es_codigo_padre(codigo, cod_prev):
                        cuenta_padre = inst
                        break

                # TITULO si parece agrupadora (pocos segmentos o termina en 00-00)
                partes = [p for p in codigo.split('-') if p.strip()]
                es_titulo = len(partes) < 5 or (len(partes) >= 2 and partes[-1] == '00' and partes[-2] == '00')
                tipo = 'TITULO' if es_titulo else 'DETALLE'

                cuenta_obj, created = CuentaContable.objects.update_or_create(
                    codigo=codigo,
                    empresa=empresa,
                    defaults={
                        'nombre': nombre,
                        'grupo': grupo,
                        'cuenta_padre': cuenta_padre,
                        'nivel': nivel,
                        'tipo': tipo,
                        'naturaleza': naturaleza,
                        'descripcion': None,
                        'acepta_movimiento': True,
                        'requiere_centro_costo': False,
                        'requiere_tercero': False,
                        'is_active': True,
                    },
                )
                mapa_codigo_a_cuenta[codigo] = cuenta_obj
                if created:
                    total_new += 1
        self.stdout.write(self.style.SUCCESS(f'Catálogo cargado. Cuentas nuevas: {total_new}, total filas: {len(filas)}.'))
