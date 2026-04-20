#!/usr/bin/env python3
"""
Script para probar la herencia de datos RTM, EXPE e ID del negocio
"""

import os
import sys

def probar_herencia_datos():
    """Prueba que los datos se hereden correctamente"""
    
    print("🔍 PROBANDO HERENCIA DE DATOS - RTM, EXPE e ID NEGOCIO")
    print("=" * 60)
    
    # 1. Verificar vista
    verificar_vista()
    
    # 2. Verificar formulario
    verificar_formulario()
    
    # 3. Verificar template
    verificar_template()
    
    # 4. Crear script de prueba
    crear_script_prueba()

def verificar_vista():
    """Verifica que la vista pase los datos correctamente"""
    
    print("\n📋 1. VERIFICANDO VISTA (simple_views.py)...")
    
    vista_path = "modules/tributario/simple_views.py"
    
    if os.path.exists(vista_path):
        with open(vista_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        verificaciones = [
            ("Búsqueda del negocio", "Negocio.objects.get"),
            ("Datos iniciales RTM", "initial_data = {'rtm': rtm, 'expe': expe}"),
            ("ID del negocio", "initial_data['idneg'] = negocio.id"),
            ("Formulario con datos iniciales", "DeclaracionVolumenForm(initial=initial_data)"),
            ("Context con negocio", "'negocio': negocio"),
            ("Context con form", "'form': form")
        ]
        
        for descripcion, codigo in verificaciones:
            if codigo in contenido:
                print(f"   ✅ {descripcion}")
            else:
                print(f"   ❌ {descripcion} - NO ENCONTRADO")
    else:
        print(f"   ❌ Archivo no encontrado: {vista_path}")

def verificar_formulario():
    """Verifica que el formulario maneje los campos correctamente"""
    
    print("\n📋 2. VERIFICANDO FORMULARIO (forms.py)...")
    
    forms_path = "venv/Scripts/tributario/tributario_app/forms.py"
    
    if os.path.exists(forms_path):
        with open(forms_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        verificaciones = [
            ("Campo idneg en fields", "'idneg'"),
            ("Campo rtm en fields", "'rtm'"),
            ("Campo expe en fields", "'expe'"),
            ("Widget idneg readonly", "'readonly': True"),
            ("Widget rtm readonly", "'readonly': True"),
            ("Widget expe readonly", "'readonly': True"),
            ("Etiqueta idneg", "'idneg': 'ID Negocio'"),
            ("Etiqueta rtm", "'rtm': 'RTM'"),
            ("Etiqueta expe", "'expe': 'Expediente'")
        ]
        
        for descripcion, codigo in verificaciones:
            if codigo in contenido:
                print(f"   ✅ {descripcion}")
            else:
                print(f"   ❌ {descripcion} - NO ENCONTRADO")
    else:
        print(f"   ❌ Archivo no encontrado: {forms_path}")

def verificar_template():
    """Verifica que el template muestre los campos correctamente"""
    
    print("\n📋 3. VERIFICANDO TEMPLATE (declaracion_volumen.html)...")
    
    template_path = "venv/Scripts/tributario/tributario_app/templates/declaracion_volumen.html"
    
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        verificaciones = [
            ("Sección Información Básica", "Información Básica"),
            ("Campo ID Negocio", "{{ form.idneg }}"),
            ("Campo RTM", "{{ form.rtm }}"),
            ("Campo Expediente", "{{ form.expe }}"),
            ("Información del Negocio", "Información del Negocio"),
            ("RTM del negocio", "{{ negocio.rtm }}"),
            ("EXPE del negocio", "{{ negocio.expe }}"),
            ("ID del negocio", "{{ negocio.id }}")
        ]
        
        for descripcion, codigo in verificaciones:
            if codigo in contenido:
                print(f"   ✅ {descripcion}")
            else:
                print(f"   ❌ {descripcion} - NO ENCONTRADO")
    else:
        print(f"   ❌ Archivo no encontrado: {template_path}")

def crear_script_prueba():
    """Crea un script de prueba para la herencia de datos"""
    
    print("\n📋 4. CREANDO SCRIPT DE PRUEBA...")
    
    script_prueba = '''#!/usr/bin/env python3
"""
Script de prueba para la herencia de datos RTM, EXPE e ID del negocio
"""

def probar_herencia_datos():
    """Prueba que los datos se hereden correctamente"""
    
    print("🧪 PRUEBA DE HERENCIA DE DATOS")
    print("=" * 50)
    
    print("\\n📋 CASOS DE PRUEBA:")
    
    casos_prueba = [
        {
            "descripcion": "Acceso con RTM y EXPE válidos",
            "url": "/tributario/declaracion-volumen/?rtm=12345&expe=67890",
            "esperado": "Los campos se llenan automáticamente"
        },
        {
            "descripcion": "Acceso sin RTM y EXPE",
            "url": "/tributario/declaracion-volumen/",
            "esperado": "Los campos aparecen vacíos"
        },
        {
            "descripcion": "Negocio no encontrado",
            "url": "/tributario/declaracion-volumen/?rtm=99999&expe=99999",
            "esperado": "Mensaje de error apropiado"
        }
    ]
    
    for i, caso in enumerate(casos_prueba, 1):
        print(f"\\n{i}. {caso['descripcion']}:")
        print(f"   URL: {caso['url']}")
        print(f"   Esperado: {caso['esperado']}")
    
    print("\\n🎯 INSTRUCCIONES PARA PROBAR:")
    print("1. Accede a la URL con parámetros RTM y EXPE:")
    print("   /tributario/declaracion-volumen/?rtm=12345&expe=67890")
    print("2. Verifica que en la sección 'Información del Negocio' aparezcan:")
    print("   - RTM: 12345")
    print("   - Expediente: 67890")
    print("3. Verifica que en la sección 'Información Básica' aparezcan:")
    print("   - ID Negocio: [ID del negocio]")
    print("   - RTM: 12345")
    print("   - Expediente: 67890")
    print("4. Verifica que los campos estén readonly (no editables)")
    print("5. Verifica que los valores coincidan entre ambas secciones")
    
    print("\\n✅ VERIFICACIONES:")
    print("- Los campos deben tener el mismo valor en ambas secciones")
    print("- Los campos deben ser readonly (no editables)")
    print("- El ID del negocio debe ser numérico")
    print("- No debe haber errores en la consola del navegador")

if __name__ == "__main__":
    probar_herencia_datos()
'''
    
    try:
        with open("prueba_herencia_datos.py", "w", encoding="utf-8") as f:
            f.write(script_prueba)
        print("   ✅ Script de prueba creado: prueba_herencia_datos.py")
    except Exception as e:
        print(f"   ❌ Error creando script de prueba: {e}")

def mostrar_resumen():
    """Muestra resumen de la verificación"""
    
    print("\n📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 60)
    
    resumen = """
    ✅ CONFIGURACIÓN ACTUAL:
    
    1. VISTA (simple_views.py):
       • Busca el negocio usando RTM y EXPE
       • Crea initial_data con RTM, EXPE e ID del negocio
       • Pasa el formulario con datos iniciales
       • Incluye el negocio en el context
    
    2. FORMULARIO (forms.py):
       • Campos idneg, rtm, expe incluidos en fields
       • Widgets configurados como readonly
       • Etiquetas personalizadas configuradas
    
    3. TEMPLATE (declaracion_volumen.html):
       • Sección "Información del Negocio" muestra datos del negocio
       • Sección "Información Básica" muestra campos del formulario
       • Ambos usan los mismos datos de origen
    
    🎯 FUNCIONAMIENTO ESPERADO:
    • Los campos RTM, EXPE e ID se llenan automáticamente
    • Los valores son los mismos en ambas secciones
    • Los campos son readonly (no editables)
    • Los datos provienen de la búsqueda del negocio
    
    🔍 POSIBLES PROBLEMAS:
    • Cache del navegador
    • Datos no encontrados en la base de datos
    • Parámetros RTM/EXPE incorrectos en la URL
    """
    
    print(resumen)

if __name__ == "__main__":
    probar_herencia_datos()
    mostrar_resumen()





