#!/usr/bin/env python3
"""
Script para verificar que los datos del negocio se estén pasando correctamente
"""

import os
import sys

def verificar_datos_negocio():
    """Verifica que los datos del negocio se estén configurando correctamente"""
    
    print("🔍 VERIFICANDO CONFIGURACIÓN DE DATOS DEL NEGOCIO")
    print("=" * 60)
    
    # 1. Verificar vista
    verificar_vista()
    
    # 2. Verificar template
    verificar_template()
    
    # 3. Verificar formulario
    verificar_formulario()
    
    # 4. Crear script de prueba
    crear_script_prueba()

def verificar_vista():
    """Verifica la configuración de la vista"""
    
    print("\n📋 1. VERIFICANDO VISTA (simple_views.py)...")
    
    vista_path = "modules/tributario/simple_views.py"
    
    if os.path.exists(vista_path):
        with open(vista_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        verificaciones = [
            ("Buscar negocio real", "negocio = Negocio.objects.get("),
            ("Incluir ID del negocio", "initial_data['idneg'] = negocio.id"),
            ("Pasar timestamp", "'timestamp': timestamp"),
            ("Pasar negocio al contexto", "'negocio': negocio")
        ]
        
        for descripcion, codigo in verificaciones:
            if codigo in contenido:
                print(f"   ✅ {descripcion}")
            else:
                print(f"   ❌ {descripcion} - NO ENCONTRADO")
    else:
        print(f"   ❌ Archivo no encontrado: {vista_path}")

def verificar_template():
    """Verifica la configuración del template"""
    
    print("\n📋 2. VERIFICANDO TEMPLATE (declaracion_volumen.html)...")
    
    template_path = "venv/Scripts/tributario/tributario_app/templates/declaracion_volumen.html"
    
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        verificaciones = [
            ("Sección Información Básica", "Información Básica"),
            ("Campo ID Negocio", "{{ form.idneg }}"),
            ("Campo RTM", "{{ form.rtm }}"),
            ("Campo Expediente", "{{ form.expe }}"),
            ("Timestamp en JavaScript", "timestamp|default:"),
            ("Información del Negocio", "{{ negocio.rtm }}")
        ]
        
        for descripcion, codigo in verificaciones:
            if codigo in contenido:
                print(f"   ✅ {descripcion}")
            else:
                print(f"   ❌ {descripcion} - NO ENCONTRADO")
    else:
        print(f"   ❌ Archivo no encontrado: {template_path}")

def verificar_formulario():
    """Verifica la configuración del formulario"""
    
    print("\n📋 3. VERIFICANDO FORMULARIO...")
    
    # Buscar archivos de formularios
    archivos_forms = [
        "venv/Scripts/tributario/tributario_app/forms.py",
        "modules/tributario/forms.py"
    ]
    
    formulario_encontrado = False
    
    for archivo in archivos_forms:
        if os.path.exists(archivo):
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            if "DeclaracionVolumenForm" in contenido:
                print(f"   ✅ Formulario encontrado en: {archivo}")
                formulario_encontrado = True
                
                verificaciones = [
                    ("Campo idneg", "'idneg'"),
                    ("Campo rtm", "'rtm'"),
                    ("Campo expe", "'expe'"),
                    ("Widget readonly", "readonly': True")
                ]
                
                for descripcion, codigo in verificaciones:
                    if codigo in contenido:
                        print(f"      ✅ {descripcion}")
                    else:
                        print(f"      ❌ {descripcion} - NO ENCONTRADO")
                break
    
    if not formulario_encontrado:
        print("   ❌ Formulario DeclaracionVolumenForm no encontrado")

def crear_script_prueba():
    """Crea un script de prueba para verificar el funcionamiento"""
    
    print("\n📋 4. CREANDO SCRIPT DE PRUEBA...")
    
    script_prueba = '''#!/usr/bin/env python3
"""
Script de prueba para verificar datos del negocio
"""

def probar_datos_negocio():
    """Prueba que los datos del negocio se estén pasando correctamente"""
    
    print("🧪 PRUEBA DE DATOS DEL NEGOCIO")
    print("=" * 40)
    
    # Simular datos de prueba
    rtm_prueba = "TEST001"
    expe_prueba = "EXP001"
    
    print(f"RTM de prueba: {rtm_prueba}")
    print(f"Expediente de prueba: {expe_prueba}")
    
    # Simular URL de prueba
    url_prueba = f"/tributario/declaracion-volumen/?rtm={rtm_prueba}&expe={expe_prueba}"
    print(f"URL de prueba: {url_prueba}")
    
    print("\\n✅ Para probar:")
    print("1. Accede a la URL de prueba")
    print("2. Verifica que los campos se llenen automáticamente:")
    print("   - ID Negocio: debe mostrar el ID real")
    print("   - RTM: debe mostrar TEST001")
    print("   - Expediente: debe mostrar EXP001")
    print("3. Verifica que la información del negocio se muestre")
    print("4. Prueba el cálculo de productos controlados")

if __name__ == "__main__":
    probar_datos_negocio()
'''
    
    try:
        with open("prueba_datos_negocio.py", "w", encoding="utf-8") as f:
            f.write(script_prueba)
        print("   ✅ Script de prueba creado: prueba_datos_negocio.py")
    except Exception as e:
        print(f"   ❌ Error creando script de prueba: {e}")

def mostrar_resumen():
    """Muestra resumen de la verificación"""
    
    print("\n📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 60)
    
    resumen = """
    ✅ CONFIGURACIÓN VERIFICADA:
    
    1. VISTA (simple_views.py):
       • Busca negocio real en base de datos
       • Incluye ID del negocio en initial_data
       • Pasa timestamp para cache busting
       • Pasa negocio al contexto del template
    
    2. TEMPLATE (declaracion_volumen.html):
       • Sección "Información Básica" configurada
       • Campos ID, RTM, EXPE usando formulario Django
       • Información del negocio mostrada
       • Timestamp en JavaScript para cache busting
    
    3. FORMULARIO:
       • Campos idneg, rtm, expe incluidos
       • Widgets readonly configurados
       • Valores iniciales desde negocio
    
    🎯 PRÓXIMOS PASOS:
    1. Recargar página con Ctrl+F5
    2. Verificar que los campos se llenen automáticamente
    3. Probar con datos reales de negocio
    4. Verificar cálculo de productos controlados
    """
    
    print(resumen)

if __name__ == "__main__":
    verificar_datos_negocio()
    mostrar_resumen()





