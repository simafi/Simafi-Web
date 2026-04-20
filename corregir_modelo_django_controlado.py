#!/usr/bin/env python3
"""
Script para corregir el modelo Django y todas las referencias de 'cocontrolado' a 'controlado'
"""

import os
import shutil
from pathlib import Path

def buscar_archivos_django():
    """Busca archivos Django que pueden contener referencias a cocontrolado"""
    
    rutas_django = [
        "c:/simafiweb/venv/Scripts/tributario/tributario_app/models.py",
        "c:/simafiweb/venv/Scripts/tributario/tributario_app/forms.py", 
        "c:/simafiweb/venv/Scripts/tributario/tributario_app/views.py",
        "c:/simafiweb/venv/Scripts/tributario/modules/tributario/models.py",
        "c:/simafiweb/venv/Scripts/tributario/modules/tributario/forms.py",
        "c:/simafiweb/venv/Scripts/tributario/modules/tributario/views.py",
        "c:/simafiweb/venv/Scripts/tributario/modules/tributario/views_clean.py"
    ]
    
    archivos_encontrados = []
    for ruta in rutas_django:
        if Path(ruta).exists():
            archivos_encontrados.append(ruta)
            print(f"✅ Encontrado: {ruta}")
        else:
            print(f"❌ No existe: {ruta}")
    
    return archivos_encontrados

def crear_correccion_modelo():
    """Crea el código corregido para el modelo Django"""
    
    modelo_corregido = '''# MODELO DJANGO CORREGIDO - models.py
# Cambiar 'cocontrolado' por 'controlado'

from django.db import models

class Declara(models.Model):
    id = models.AutoField(primary_key=True)
    idneg = models.IntegerField(default=0)
    rtm = models.CharField(max_length=20, default='')
    expe = models.CharField(max_length=10, blank=True, null=True)
    ano = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tipo = models.DecimalField(max_digits=1, decimal_places=0, default=0)
    mes = models.DecimalField(max_digits=4, decimal_places=0, default=0)
    ventai = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    ventac = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    ventas = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    valorexcento = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    
    # CORREGIDO: usar 'controlado' en lugar de 'cocontrolado'
    controlado = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    
    unidad = models.DecimalField(max_digits=11, decimal_places=0, default=0)
    factor = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    fechssys = models.DateTimeField(blank=True, null=True)
    usuario = models.CharField(max_length=50, blank=True, null=True)
    impuesto = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    class Meta:
        db_table = 'declara'
        managed = False  # Django no gestiona esta tabla
        
    def __str__(self):
        return f"Declara {self.id} - RTM: {self.rtm}"
'''
    
    with open("c:/simafiweb/modelo_declara_corregido.py", 'w', encoding='utf-8') as f:
        f.write(modelo_corregido)
    
    print("✅ Modelo corregido creado: modelo_declara_corregido.py")

def crear_correccion_forms():
    """Crea el código corregido para los formularios Django"""
    
    forms_corregido = '''# FORMULARIOS DJANGO CORREGIDOS - forms.py
# Cambiar 'cocontrolado' por 'controlado'

from django import forms
from .models import Declara

class DeclaraForm(forms.ModelForm):
    class Meta:
        model = Declara
        fields = [
            'rtm', 'expe', 'ano', 'tipo', 'mes',
            'ventai', 'ventac', 'ventas', 'valorexcento',
            'controlado',  # CORREGIDO: era 'cocontrolado'
            'unidad', 'factor', 'usuario', 'impuesto'
        ]
        
        widgets = {
            'ventai': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ventas Industria',
                'data-format': 'decimal-16-2'
            }),
            'ventac': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ventas Comercio',
                'data-format': 'decimal-16-2'
            }),
            'ventas': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ventas Servicios', 
                'data-format': 'decimal-16-2'
            }),
            'controlado': forms.TextInput(attrs={  # CORREGIDO
                'class': 'form-control',
                'placeholder': 'Valor Controlado',
                'data-format': 'decimal-16-2'
            }),
            'impuesto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Impuesto Calculado',
                'data-format': 'decimal-12-2',
                'readonly': True
            })
        }
        
        labels = {
            'ventai': 'Ventas Industria',
            'ventac': 'Ventas Comercio', 
            'ventas': 'Ventas Servicios',
            'controlado': 'Valor Controlado',  # CORREGIDO
            'impuesto': 'Impuesto ICS'
        }
'''
    
    with open("c:/simafiweb/forms_declara_corregido.py", 'w', encoding='utf-8') as f:
        f.write(forms_corregido)
    
    print("✅ Formularios corregidos creados: forms_declara_corregido.py")

def crear_correccion_views():
    """Crea el código corregido para las vistas Django"""
    
    views_corregido = '''# VISTAS DJANGO CORREGIDAS - views.py
# Cambiar todas las referencias de 'cocontrolado' por 'controlado'

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Declara
from .forms import DeclaraForm

def declaracion_volumen(request):
    """Vista para declaración de volumen corregida"""
    
    rtm = request.GET.get('rtm')
    expe = request.GET.get('expe')
    
    # Buscar registro existente
    declara = None
    if rtm and expe:
        try:
            declara = Declara.objects.get(rtm=rtm, expe=expe)
        except Declara.DoesNotExist:
            declara = None
    
    if request.method == 'POST':
        form = DeclaraForm(request.POST, instance=declara)
        if form.is_valid():
            # Procesar datos corregidos
            instance = form.save(commit=False)
            
            # Calcular impuesto basado en campos corregidos
            total_ventas = (
                (instance.ventai or 0) +
                (instance.ventac or 0) + 
                (instance.ventas or 0) +
                (instance.controlado or 0)  # CORREGIDO: era cocontrolado
            )
            
            # Calcular impuesto ICS
            instance.impuesto = calcular_impuesto_ics(total_ventas)
            instance.save()
            
            return JsonResponse({
                'success': True,
                'impuesto': float(instance.impuesto),
                'total_ventas': float(total_ventas)
            })
    else:
        form = DeclaraForm(instance=declara)
    
    context = {
        'form': form,
        'rtm': rtm,
        'expe': expe,
        'declara': declara
    }
    
    return render(request, 'declaracion_volumen.html', context)

def calcular_impuesto_ics(total_ventas):
    """Calcula el impuesto ICS basado en el total de ventas"""
    
    if not total_ventas or total_ventas <= 0:
        return 0
    
    # Tarifas progresivas ICS
    tarifas = [
        (1000000, 0.002),      # 0-1M: 0.2%
        (5000000, 0.004),      # 1M-5M: 0.4%
        (10000000, 0.003),     # 5M-10M: 0.3%
        (20000000, 0.003),     # 10M-20M: 0.3%
        (30000000, 0.002),     # 20M-30M: 0.2%
        (float('inf'), 0.0015) # >30M: 0.15%
    ]
    
    impuesto_total = 0
    base_anterior = 0
    
    for limite, tarifa in tarifas:
        if total_ventas <= base_anterior:
            break
            
        base_gravable = min(total_ventas, limite) - base_anterior
        impuesto_tramo = base_gravable * tarifa
        impuesto_total += impuesto_tramo
        
        base_anterior = limite
        
        if total_ventas <= limite:
            break
    
    return round(impuesto_total, 2)
'''
    
    with open("c:/simafiweb/views_declara_corregido.py", 'w', encoding='utf-8') as f:
        f.write(views_corregido)
    
    print("✅ Vistas corregidas creadas: views_declara_corregido.py")

def crear_migracion_django():
    """Crea una migración Django para renombrar el campo"""
    
    migracion = '''# Migración Django para renombrar campo cocontrolado -> controlado
# Archivo: XXXX_rename_cocontrolado_to_controlado.py

from django.db import migrations

class Migration(migrations.Migration):
    
    dependencies = [
        ('tributario_app', '0037_tarifasimptoics_alter_planarbitrio_options_and_more'),
    ]
    
    operations = [
        # Renombrar campo en el modelo (si existe cocontrolado)
        migrations.RenameField(
            model_name='declara',
            old_name='cocontrolado',
            new_name='controlado',
        ),
        
        # O agregar el campo si no existe
        # migrations.AddField(
        #     model_name='declara',
        #     name='controlado',
        #     field=models.DecimalField(decimal_places=2, default=0.0, max_digits=16),
        # ),
    ]
    
# NOTA: Esta migración puede no ser necesaria si la tabla ya tiene el campo 'controlado'
# En ese caso, solo actualizar el modelo Django para que coincida con la BD
'''
    
    with open("c:/simafiweb/migracion_rename_controlado.py", 'w', encoding='utf-8') as f:
        f.write(migracion)
    
    print("✅ Migración creada: migracion_rename_controlado.py")

def crear_script_aplicar_correcciones():
    """Crea script para aplicar todas las correcciones"""
    
    script = '''#!/usr/bin/env python3
"""
Script para aplicar correcciones de 'cocontrolado' -> 'controlado' en Django
"""

import os
import shutil
from pathlib import Path

def aplicar_correcciones():
    """Aplica las correcciones a los archivos Django"""
    
    # Archivos a corregir
    archivos_django = [
        "c:/simafiweb/venv/Scripts/tributario/tributario_app/models.py",
        "c:/simafiweb/venv/Scripts/tributario/tributario_app/forms.py",
        "c:/simafiweb/venv/Scripts/tributario/tributario_app/views.py",
        "c:/simafiweb/venv/Scripts/tributario/modules/tributario/models.py",
        "c:/simafiweb/venv/Scripts/tributario/modules/tributario/forms.py", 
        "c:/simafiweb/venv/Scripts/tributario/modules/tributario/views.py"
    ]
    
    correcciones = [
        ("cocontrolado", "controlado"),
        ("'cocontrolado'", "'controlado'"),
        ('"cocontrolado"', '"controlado"'),
        ("Cocontrolado", "Controlado")
    ]
    
    archivos_corregidos = 0
    
    for archivo_path in archivos_django:
        archivo = Path(archivo_path)
        
        if archivo.exists():
            print(f"🔧 Corrigiendo: {archivo}")
            
            # Leer contenido
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Aplicar correcciones
            contenido_original = contenido
            for buscar, reemplazar in correcciones:
                contenido = contenido.replace(buscar, reemplazar)
            
            # Guardar si hubo cambios
            if contenido != contenido_original:
                # Hacer backup
                backup_path = archivo.with_suffix('.backup_controlado')
                shutil.copy2(archivo, backup_path)
                print(f"  📁 Backup: {backup_path}")
                
                # Guardar corregido
                with open(archivo, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                
                archivos_corregidos += 1
                print(f"  ✅ Corregido")
            else:
                print(f"  ℹ️ Sin cambios necesarios")
        else:
            print(f"❌ No existe: {archivo}")
    
    print(f"\\n✅ Correcciones aplicadas a {archivos_corregidos} archivos")
    
    return archivos_corregidos > 0

if __name__ == "__main__":
    print("🔧 APLICANDO CORRECCIONES DJANGO: cocontrolado -> controlado")
    print("=" * 60)
    
    if aplicar_correcciones():
        print("\\n🚀 PRÓXIMOS PASOS:")
        print("1. Reiniciar servidor Django")
        print("2. Probar URL: /tributario/declaracion-volumen/")
        print("3. Verificar que no hay más errores OperationalError")
    else:
        print("\\n⚠️ No se aplicaron correcciones")
'''
    
    with open("c:/simafiweb/aplicar_correcciones_django.py", 'w', encoding='utf-8') as f:
        f.write(script)
    
    print("✅ Script aplicación creado: aplicar_correcciones_django.py")

def main():
    print("🔧 CORRIGIENDO MODELO DJANGO Y REFERENCIAS")
    print("=" * 50)
    
    print("\n🔍 Buscando archivos Django...")
    archivos = buscar_archivos_django()
    
    print(f"\n📋 Encontrados {len(archivos)} archivos Django")
    
    print("\n🔧 Creando correcciones...")
    crear_correccion_modelo()
    crear_correccion_forms()
    crear_correccion_views()
    crear_migracion_django()
    crear_script_aplicar_correcciones()
    
    print("\n" + "=" * 50)
    print("✅ CORRECCIONES PREPARADAS")
    
    print("\n📝 ARCHIVOS CREADOS:")
    print("- modelo_declara_corregido.py")
    print("- forms_declara_corregido.py") 
    print("- views_declara_corregido.py")
    print("- migracion_rename_controlado.py")
    print("- aplicar_correcciones_django.py")
    
    print("\n🚀 EJECUTAR:")
    print("python aplicar_correcciones_django.py")
    
    print("\n⚠️ IMPORTANTE:")
    print("- Se crearán backups automáticamente")
    print("- Reiniciar servidor Django después")
    print("- Probar formulario declaración volumen")

if __name__ == "__main__":
    main()
