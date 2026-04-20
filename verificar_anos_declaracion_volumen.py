#!/usr/bin/env python3
"""
Script para verificar y corregir la implementación del combobox de años
en el formulario declaracion_volumen usando la tabla anos
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')

try:
    django.setup()
    from venv.Scripts.tributario.tributario_app.models import Anos, DeclaracionVolumen
    from venv.Scripts.tributario.tributario_app.forms import DeclaracionVolumenForm
    print("✅ Django configurado correctamente")
except Exception as e:
    print(f"❌ Error configurando Django: {e}")
    sys.exit(1)

def verificar_modelo_anos():
    """Verificar que el modelo Anos existe y tiene la estructura correcta"""
    print("\n=== VERIFICANDO MODELO ANOS ===")
    
    try:
        # Verificar estructura del modelo
        campos = Anos._meta.get_fields()
        print("Campos del modelo Anos:")
        for campo in campos:
            print(f"  - {campo.name}: {type(campo).__name__}")
        
        # Verificar datos existentes
        total_anos = Anos.objects.count()
        print(f"\nTotal de años en la base de datos: {total_anos}")
        
        if total_anos > 0:
            anos_existentes = Anos.objects.all().order_by('-ano')
            print("Años disponibles:")
            for ano in anos_existentes:
                print(f"  - {ano.ano}")
        else:
            print("⚠️  No hay datos en la tabla anos")
            
        return True
        
    except Exception as e:
        print(f"❌ Error verificando modelo Anos: {e}")
        return False

def verificar_formulario():
    """Verificar que el formulario carga correctamente los años"""
    print("\n=== VERIFICANDO FORMULARIO ===")
    
    try:
        form = DeclaracionVolumenForm()
        
        # Verificar si el campo ano existe
        if 'ano' in form.fields:
            print("✅ Campo 'ano' encontrado en el formulario")
            
            # Verificar las opciones del campo
            ano_field = form.fields['ano']
            if hasattr(ano_field.widget, 'choices'):
                choices = ano_field.widget.choices
                print(f"Opciones del combobox de años: {len(choices)} elementos")
                for choice in choices:
                    print(f"  - Valor: '{choice[0]}', Texto: '{choice[1]}'")
            else:
                print("⚠️  El campo año no tiene opciones configuradas")
        else:
            print("❌ Campo 'ano' no encontrado en el formulario")
            
        return True
        
    except Exception as e:
        print(f"❌ Error verificando formulario: {e}")
        return False

def crear_anos_ejemplo():
    """Crear años de ejemplo si no existen"""
    print("\n=== CREANDO AÑOS DE EJEMPLO ===")
    
    anos_ejemplo = [2020, 2021, 2022, 2023, 2024, 2025]
    
    for ano in anos_ejemplo:
        try:
            ano_obj, created = Anos.objects.get_or_create(ano=ano)
            if created:
                print(f"✅ Año {ano} creado")
            else:
                print(f"ℹ️  Año {ano} ya existe")
        except Exception as e:
            print(f"❌ Error creando año {ano}: {e}")

def generar_vista_corregida():
    """Generar una vista corregida para declaracion_volumen"""
    print("\n=== GENERANDO VISTA CORREGIDA ===")
    
    vista_corregida = '''
def declaracion_volumen(request):
    """Vista para el formulario de declaración de volumen de ventas"""
    from .models import DeclaracionVolumen, Negocio, TarifasICS, Anos
    from .forms import DeclaracionVolumenForm
    from decimal import Decimal
    
    # Inicializar variables
    negocio = None
    tarifas_ics = None
    
    # Obtener años disponibles de la tabla anos
    anos_disponibles = Anos.objects.all().order_by('-ano')
    
    # Obtener parámetros de la URL
    rtm = request.GET.get('rtm', '')
    expe = request.GET.get('expe', '')
    
    # Buscar negocio si se proporcionan RTM y EXPE
    if rtm and expe:
        try:
            negocio = Negocio.objects.get(rtm=rtm, expe=expe)
        except Negocio.DoesNotExist:
            negocio = None
    
    # Buscar declaración existente
    declaracion = None
    if rtm and expe:
        try:
            declaracion = DeclaracionVolumen.objects.get(rtm=rtm, expe=expe)
        except DeclaracionVolumen.DoesNotExist:
            declaracion = None
    
    if request.method == 'POST':
        form = DeclaracionVolumenForm(request.POST, instance=declaracion)
        if form.is_valid():
            instance = form.save(commit=False)
            
            # Asignar RTM y EXPE si están disponibles
            if rtm:
                instance.rtm = rtm
            if expe:
                instance.expe = expe
            
            instance.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Declaración guardada exitosamente'
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    else:
        form = DeclaracionVolumenForm(instance=declaracion)
    
    context = {
        'form': form,
        'negocio': negocio,
        'rtm': rtm,
        'expe': expe,
        'declaracion': declaracion,
        'anos_disponibles': anos_disponibles,  # ← IMPORTANTE: Pasar años al template
        'tarifas_ics': tarifas_ics
    }
    
    return render(request, 'declaracion_volumen.html', context)
'''
    
    # Guardar vista corregida
    with open('vista_declaracion_volumen_corregida.py', 'w', encoding='utf-8') as f:
        f.write(vista_corregida)
    
    print("✅ Vista corregida guardada en 'vista_declaracion_volumen_corregida.py'")

def main():
    """Función principal"""
    print("🔍 VERIFICACIÓN DEL COMBOBOX DE AÑOS - DECLARACIÓN VOLUMEN")
    print("=" * 60)
    
    # Verificar modelo
    modelo_ok = verificar_modelo_anos()
    
    # Verificar formulario
    formulario_ok = verificar_formulario()
    
    # Si no hay años, crear algunos de ejemplo
    if modelo_ok:
        total_anos = Anos.objects.count()
        if total_anos == 0:
            crear_anos_ejemplo()
    
    # Generar vista corregida
    generar_vista_corregida()
    
    print("\n" + "=" * 60)
    print("✅ VERIFICACIÓN COMPLETADA")
    print("\nPasos siguientes:")
    print("1. Asegúrate de que la tabla 'anos' tenga datos")
    print("2. Verifica que la vista pase 'anos_disponibles' al template")
    print("3. Confirma que el template use la variable correctamente")

if __name__ == "__main__":
    main()
