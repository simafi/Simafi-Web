# -*- coding: utf-8 -*-
"""
Carga permisos y roles «acceso completo» para: Administrativo, Contabilidad, Tesorería,
Presupuestos y Configuración.

Uso (desde c:\\simafiweb\\venv\\Scripts):
    python manage.py seed_modulos_restantes_permisos

Catastro:  python manage.py seed_catastro_permisos
Tributario: python manage.py seed_tributario_permisos
"""
from django.core.management.base import BaseCommand

from core.permisos_modulos_seed import MODULOS_RESTANTES_SEED
from usuarios.models import Permiso, Rol


class Command(BaseCommand):
    help = (
        "Inserta permisos de aplicación de los módulos restantes y un rol completo por módulo."
    )

    def handle(self, *args, **options):
        total_creados = 0
        for modulo_codigo, permisos_tuples, nombre_rol in MODULOS_RESTANTES_SEED:
            creados_mod = 0
            for codigo, nombre in permisos_tuples:
                _, created = Permiso.objects.update_or_create(
                    codigo=codigo,
                    defaults={
                        "nombre": nombre,
                        "modulo": modulo_codigo,
                        "is_active": True,
                    },
                )
                if created:
                    creados_mod += 1
                    total_creados += 1

            codigos = [t[0] for t in permisos_tuples]
            permisos = list(Permiso.objects.filter(codigo__in=codigos))
            rol, _ = Rol.objects.get_or_create(
                nombre=nombre_rol,
                defaults={
                    "descripcion": f"Incluye todos los permisos del módulo {modulo_codigo}.",
                    "is_active": True,
                },
            )
            rol.permisos.set(permisos)
            rol.is_active = True
            rol.save(update_fields=["is_active", "updated_at"])

            self.stdout.write(
                self.style.SUCCESS(
                    f"  [{modulo_codigo}] {len(permisos_tuples)} permisos "
                    f"({creados_mod} nuevos) -> rol \"{nombre_rol}\""
                )
            )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Listo. {total_creados} permisos nuevos en total (resto actualizados)."
            )
        )
        self.stdout.write(
            "Asigne los roles en «Usuarios del sistema» o cree roles parciales en «Roles»."
        )
