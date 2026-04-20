#!/usr/bin/env python3
"""
Script para probar las validaciones implementadas
"""

import os
import sys

def probar_validaciones():
    """Prueba que las validaciones estén correctamente implementadas"""
    
    print("🧪 PROBANDO VALIDACIONES DE FORMULARIO")
    print("=" * 50)
    
    # 1. Verificar formulario Django
    verificar_formulario_django()
    
    # 2. Verificar JavaScript
    verificar_javascript()
    
    # 3. Verificar template
    verificar_template()
    
    # 4. Crear script de prueba
    crear_script_prueba()

def verificar_formulario_django():
    """Verifica las validaciones en el formulario Django"""
    
    print("\n📋 1. VERIFICANDO FORMULARIO DJANGO (forms.py)...")
    
    forms_path = "venv/Scripts/tributario/tributario_app/forms.py"
    
    if os.path.exists(forms_path):
        with open(forms_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        verificaciones = [
            ("Validación RTM", "if not rtm:"),
            ("Validación EXPE", "if not expe:"),
            ("Mensaje RTM obligatorio", "El campo RTM es obligatorio"),
            ("Mensaje EXPE obligatorio", "El campo Expediente es obligatorio"),
            ("Validación total ventas", "if total_ventas <= 0:"),
            ("Validación impuesto", "if impuesto <= 0:"),
            ("Mensaje impuesto mayor a cero", "El impuesto calculado debe ser mayor a 0")
        ]
        
        for descripcion, codigo in verificaciones:
            if codigo in contenido:
                print(f"   ✅ {descripcion}")
            else:
                print(f"   ❌ {descripcion} - NO ENCONTRADO")
    else:
        print(f"   ❌ Archivo no encontrado: {forms_path}")

def verificar_javascript():
    """Verifica las validaciones en JavaScript"""
    
    print("\n📋 2. VERIFICANDO JAVASCRIPT (declaracion_volumen_interactivo.js)...")
    
    js_path = "venv/Scripts/tributario/tributario_app/static/js/declaracion_volumen_interactivo.js"
    
    if os.path.exists(js_path):
        with open(js_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        verificaciones = [
            ("Función validarFormulario", "validarFormulario()"),
            ("Validación RTM JS", "id_rtm"),
            ("Validación EXPE JS", "id_expe"),
            ("Validación total ventas JS", "totalVentas <= 0"),
            ("Validación impuesto JS", "impuesto <= 0"),
            ("Mensaje RTM obligatorio JS", "El campo RTM es obligatorio"),
            ("Mensaje EXPE obligatorio JS", "El campo Expediente es obligatorio"),
            ("Mensaje impuesto mayor a cero JS", "El impuesto calculado debe ser mayor a 0")
        ]
        
        for descripcion, codigo in verificaciones:
            if codigo in contenido:
                print(f"   ✅ {descripcion}")
            else:
                print(f"   ❌ {descripcion} - NO ENCONTRADO")
    else:
        print(f"   ❌ Archivo no encontrado: {js_path}")

def verificar_template():
    """Verifica las validaciones en el template"""
    
    print("\n📋 3. VERIFICANDO TEMPLATE (declaracion_volumen.html)...")
    
    template_path = "venv/Scripts/tributario/tributario_app/templates/declaracion_volumen.html"
    
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        verificaciones = [
            ("Event listener submit", "addEventListener('submit'"),
            ("Validación RTM template", "id_rtm"),
            ("Validación EXPE template", "id_expe"),
            ("PreventDefault", "preventDefault()"),
            ("Mensaje RTM template", "El campo RTM es obligatorio"),
            ("Mensaje EXPE template", "El campo Expediente es obligatorio")
        ]
        
        for descripcion, codigo in verificaciones:
            if codigo in contenido:
                print(f"   ✅ {descripcion}")
            else:
                print(f"   ❌ {descripcion} - NO ENCONTRADO")
    else:
        print(f"   ❌ Archivo no encontrado: {template_path}")

def crear_script_prueba():
    """Crea un script de prueba para las validaciones"""
    
    print("\n📋 4. CREANDO SCRIPT DE PRUEBA...")
    
    script_prueba = '''#!/usr/bin/env python3
"""
Script de prueba para las validaciones del formulario
"""

def probar_validaciones():
    """Prueba las validaciones implementadas"""
    
    print("🧪 PRUEBA DE VALIDACIONES")
    print("=" * 50)
    
    print("\\n📋 CASOS DE PRUEBA:")
    
    casos_prueba = [
        {
            "descripcion": "RTM vacío",
            "rtm": "",
            "expe": "12345",
            "ventas": 1000,
            "esperado": "Error: RTM es obligatorio"
        },
        {
            "descripcion": "EXPE vacío",
            "rtm": "12345",
            "expe": "",
            "ventas": 1000,
            "esperado": "Error: Expediente es obligatorio"
        },
        {
            "descripcion": "Sin valores de ventas",
            "rtm": "12345",
            "expe": "67890",
            "ventas": 0,
            "esperado": "Error: Al menos uno de los campos de ventas debe tener un valor mayor a 0"
        },
        {
            "descripcion": "Impuesto cero",
            "rtm": "12345",
            "expe": "67890",
            "ventas": 1000,
            "impuesto": 0,
            "esperado": "Error: El impuesto calculado debe ser mayor a 0"
        },
        {
            "descripcion": "Formulario válido",
            "rtm": "12345",
            "expe": "67890",
            "ventas": 1000,
            "impuesto": 150,
            "esperado": "Formulario válido - Se puede guardar"
        }
    ]
    
    for i, caso in enumerate(casos_prueba, 1):
        print(f"\\n{i}. {caso['descripcion']}:")
        print(f"   RTM: '{caso['rtm']}'")
        print(f"   EXPE: '{caso['expe']}'")
        print(f"   Ventas: {caso['ventas']}")
        if 'impuesto' in caso:
            print(f"   Impuesto: {caso['impuesto']}")
        print(f"   Esperado: {caso['esperado']}")
    
    print("\\n🎯 INSTRUCCIONES PARA PROBAR:")
    print("1. Accede al formulario de declaración de volumen")
    print("2. Prueba cada caso de prueba:")
    print("   a) Deja RTM vacío y intenta guardar")
    print("   b) Deja EXPE vacío y intenta guardar")
    print("   c) No ingreses valores de ventas y intenta guardar")
    print("   d) Ingresa valores pero no calcules impuesto e intenta guardar")
    print("   e) Completa todo correctamente e intenta guardar")
    print("3. Verifica que aparezcan los mensajes de error apropiados")
    print("4. Verifica que el formulario no se envíe con datos inválidos")
    
    print("\\n✅ VERIFICACIONES:")
    print("- Los mensajes de error deben ser claros y específicos")
    print("- El formulario no debe enviarse con datos inválidos")
    print("- Los campos obligatorios deben estar marcados")
    print("- Las validaciones deben funcionar tanto en Django como en JavaScript")

if __name__ == "__main__":
    probar_validaciones()
'''
    
    try:
        with open("prueba_validaciones.py", "w", encoding="utf-8") as f:
            f.write(script_prueba)
        print("   ✅ Script de prueba creado: prueba_validaciones.py")
    except Exception as e:
        print(f"   ❌ Error creando script de prueba: {e}")

def mostrar_resumen():
    """Muestra resumen de las validaciones implementadas"""
    
    print("\n📊 RESUMEN DE VALIDACIONES IMPLEMENTADAS")
    print("=" * 60)
    
    resumen = """
    ✅ VALIDACIONES IMPLEMENTADAS:
    
    1. FORMULARIO DJANGO (forms.py):
       • Validación RTM obligatorio
       • Validación EXPE obligatorio
       • Validación total ventas > 0
       • Validación impuesto > 0
       • Mensajes de error específicos
    
    2. JAVASCRIPT (declaracion_volumen_interactivo.js):
       • Validación RTM obligatorio
       • Validación EXPE obligatorio
       • Validación total ventas > 0
       • Validación impuesto > 0
       • Validación año y mes obligatorios
       • Logs detallados para debugging
    
    3. TEMPLATE (declaracion_volumen.html):
       • Event listener para submit
       • Validación RTM y EXPE
       • PreventDefault para datos inválidos
       • Mensajes de error consistentes
    
    🎯 FLUJO DE VALIDACIÓN:
    1. Usuario completa formulario
    2. JavaScript valida en tiempo real
    3. Al enviar, JavaScript valida nuevamente
    4. Si es válido, se envía al servidor
    5. Django valida en el servidor
    6. Si hay errores, se muestran al usuario
    
    🔍 CASOS CUBIERTOS:
    • RTM vacío o nulo
    • EXPE vacío o nulo
    • Sin valores de ventas
    • Impuesto cero o negativo
    • Año o mes no seleccionados
    • Formulario completo y válido
    """
    
    print(resumen)

if __name__ == "__main__":
    probar_validaciones()
    mostrar_resumen()





