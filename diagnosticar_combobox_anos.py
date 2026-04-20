#!/usr/bin/env python3
"""
Diagnóstico completo del problema del combobox de años
"""

import os
import sys
import django

# Configurar Django
sys.path.append('C:/simafiweb/venv/Scripts/tributario')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')

def diagnosticar_problema():
    """Diagnosticar paso a paso por qué no aparecen los años"""
    
    print("🔍 DIAGNÓSTICO DEL COMBOBOX DE AÑOS")
    print("=" * 50)
    
    # 1. Verificar configuración Django
    print("\n1. Configurando Django...")
    try:
        django.setup()
        print("✅ Django configurado correctamente")
    except Exception as e:
        print(f"❌ Error configurando Django: {e}")
        return False
    
    # 2. Verificar modelo Anos
    print("\n2. Verificando modelo Anos...")
    try:
        from tributario_app.models import Anos
        print("✅ Modelo Anos importado correctamente")
        
        # Verificar estructura
        campos = [f.name for f in Anos._meta.get_fields()]
        print(f"   Campos del modelo: {campos}")
        
        # Verificar tabla en BD
        total_anos = Anos.objects.count()
        print(f"   Total registros en tabla anos: {total_anos}")
        
        if total_anos == 0:
            print("⚠️  PROBLEMA ENCONTRADO: No hay datos en la tabla anos")
            return "sin_datos"
        else:
            print("✅ Hay datos en la tabla anos")
            
            # Mostrar algunos años
            anos_sample = Anos.objects.all().order_by('-ano')[:5]
            print("   Años disponibles (muestra):")
            for ano in anos_sample:
                print(f"     - {ano.ano} (tipo: {type(ano.ano)})")
                
    except ImportError as e:
        print(f"❌ Error importando modelo Anos: {e}")
        return "modelo_no_encontrado"
    except Exception as e:
        print(f"❌ Error accediendo a datos: {e}")
        return "error_bd"
    
    # 3. Verificar formulario
    print("\n3. Verificando formulario...")
    try:
        from tributario_app.forms import DeclaracionVolumenForm
        print("✅ Formulario importado correctamente")
        
        # Crear instancia del formulario
        form = DeclaracionVolumenForm()
        
        # Verificar campo ano
        if 'ano' in form.fields:
            print("✅ Campo 'ano' existe en el formulario")
            
            # Verificar opciones del combobox
            ano_field = form.fields['ano']
            if hasattr(ano_field.widget, 'choices'):
                choices = list(ano_field.widget.choices)
                print(f"   Opciones en combobox: {len(choices)}")
                
                if len(choices) <= 1:
                    print("⚠️  PROBLEMA ENCONTRADO: Combobox solo tiene opción vacía")
                    return "formulario_sin_opciones"
                else:
                    print("✅ Combobox tiene opciones")
                    print("   Primeras opciones:")
                    for i, (value, label) in enumerate(choices[:6]):
                        print(f"     {i+1}. '{value}' → '{label}'")
            else:
                print("❌ Campo año no tiene widget de opciones")
                return "widget_incorrecto"
        else:
            print("❌ Campo 'ano' no existe en el formulario")
            return "campo_no_existe"
            
    except ImportError as e:
        print(f"❌ Error importando formulario: {e}")
        return "formulario_no_encontrado"
    except Exception as e:
        print(f"❌ Error en formulario: {e}")
        return "error_formulario"
    
    # 4. Verificar vista
    print("\n4. Verificando vista...")
    try:
        # Buscar archivo de vista
        vista_paths = [
            'C:/simafiweb/venv/Scripts/tributario/tributario_app/views.py',
            'C:/simafiweb/venv/Scripts/tributario/modules/tributario/views.py'
        ]
        
        vista_encontrada = False
        for path in vista_paths:
            if os.path.exists(path):
                print(f"✅ Archivo de vista encontrado: {path}")
                vista_encontrada = True
                
                # Leer contenido
                with open(path, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                
                # Verificar función declaracion_volumen
                if 'def declaracion_volumen(request):' in contenido:
                    print("✅ Función declaracion_volumen encontrada")
                    
                    # Verificar si importa Anos
                    if 'Anos' in contenido:
                        print("✅ Vista importa modelo Anos")
                    else:
                        print("⚠️  PROBLEMA ENCONTRADO: Vista no importa modelo Anos")
                        return "vista_sin_import"
                    
                    # Verificar si obtiene anos_disponibles
                    if 'anos_disponibles' in contenido:
                        print("✅ Vista obtiene anos_disponibles")
                    else:
                        print("⚠️  PROBLEMA ENCONTRADO: Vista no obtiene anos_disponibles")
                        return "vista_sin_anos"
                    
                    # Verificar si pasa al context
                    if "'anos_disponibles'" in contenido:
                        print("✅ Vista pasa anos_disponibles al template")
                    else:
                        print("⚠️  PROBLEMA ENCONTRADO: Vista no pasa anos_disponibles al context")
                        return "vista_sin_context"
                else:
                    print("⚠️  Función declaracion_volumen no encontrada en este archivo")
                break
        
        if not vista_encontrada:
            print("❌ No se encontró archivo de vista")
            return "vista_no_encontrada"
            
    except Exception as e:
        print(f"❌ Error verificando vista: {e}")
        return "error_vista"
    
    # 5. Verificar template
    print("\n5. Verificando template...")
    try:
        template_path = 'C:/simafiweb/venv/Scripts/tributario/tributario_app/templates/declaracion_volumen.html'
        
        if os.path.exists(template_path):
            print("✅ Template encontrado")
            
            with open(template_path, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Verificar combobox de años
            if 'id_ano' in contenido:
                print("✅ Combobox de años existe en template")
                
                # Verificar loop de años
                if '{% for ano in anos_disponibles %}' in contenido:
                    print("✅ Template usa loop de anos_disponibles")
                else:
                    print("⚠️  PROBLEMA ENCONTRADO: Template no usa loop de anos_disponibles")
                    return "template_sin_loop"
            else:
                print("❌ Combobox de años no encontrado en template")
                return "template_sin_combobox"
        else:
            print("❌ Template no encontrado")
            return "template_no_encontrado"
            
    except Exception as e:
        print(f"❌ Error verificando template: {e}")
        return "error_template"
    
    print("\n✅ DIAGNÓSTICO COMPLETADO - No se encontraron problemas obvios")
    return "ok"

def crear_solucion(problema):
    """Crear solución específica según el problema encontrado"""
    
    print(f"\n🔧 CREANDO SOLUCIÓN PARA: {problema}")
    print("=" * 50)
    
    if problema == "sin_datos":
        # Crear script para poblar datos
        script_poblar = '''
import os
import sys
import django

sys.path.append('C:/simafiweb/venv/Scripts/tributario')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from tributario_app.models import Anos

# Crear años 2015-2026
for ano in range(2015, 2027):
    Anos.objects.get_or_create(ano=ano)
    print(f"Año {ano} creado/verificado")

print(f"Total años: {Anos.objects.count()}")
'''
        with open('poblar_anos_solucion.py', 'w') as f:
            f.write(script_poblar)
        print("✅ Creado: poblar_anos_solucion.py")
        
    elif problema == "formulario_sin_opciones":
        # Corregir formulario
        formulario_corregido = '''
# Agregar al __init__ del DeclaracionVolumenForm:

def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    # Cargar años dinámicamente
    try:
        from .models import Anos
        anos_choices = [('', 'Seleccione un año')]
        for ano in Anos.objects.all().order_by('-ano'):
            anos_choices.append((str(int(ano.ano)), str(int(ano.ano))))
        
        self.fields['ano'].widget.choices = anos_choices
        print(f"Años cargados en formulario: {len(anos_choices)-1}")
        
    except Exception as e:
        print(f"Error cargando años: {e}")
'''
        with open('corregir_formulario_anos.py', 'w') as f:
            f.write(formulario_corregido)
        print("✅ Creado: corregir_formulario_anos.py")
        
    elif problema == "vista_sin_anos":
        # Corregir vista
        vista_corregida = '''
# Agregar a la función declaracion_volumen:

from .models import Anos

def declaracion_volumen(request):
    # ... código existente ...
    
    # Obtener años disponibles
    try:
        anos_disponibles = Anos.objects.all().order_by('-ano')
        print(f"Años obtenidos: {anos_disponibles.count()}")
    except Exception as e:
        print(f"Error obteniendo años: {e}")
        anos_disponibles = []
    
    context = {
        # ... otros datos ...
        'anos_disponibles': anos_disponibles,
    }
    
    return render(request, 'declaracion_volumen.html', context)
'''
        with open('corregir_vista_anos.py', 'w') as f:
            f.write(vista_corregida)
        print("✅ Creado: corregir_vista_anos.py")

def main():
    """Función principal de diagnóstico"""
    problema = diagnosticar_problema()
    
    if problema != "ok":
        crear_solucion(problema)
        
        print(f"\n🎯 PROBLEMA IDENTIFICADO: {problema}")
        print("\nSoluciones creadas. Ejecutar los archivos generados.")
    else:
        print("\n✅ No se encontraron problemas. El combobox debería funcionar.")
        print("\nSi aún no funciona, verificar:")
        print("1. Servidor Django reiniciado")
        print("2. Migraciones aplicadas")
        print("3. Cache del navegador limpio")

if __name__ == "__main__":
    main()
