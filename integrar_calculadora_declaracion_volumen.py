#!/usr/bin/env python
"""
Integración de calculadora interactiva en el formulario declaracion_volumen
"""

import os
import shutil

def integrar_calculadora_declaracion():
    """
    Integra la calculadora interactiva en el formulario declaracion_volumen
    """
    print("🔧 INTEGRANDO CALCULADORA EN DECLARACIÓN VOLUMEN")
    print("=" * 50)
    
    # Rutas de archivos
    js_source = r"c:\simafiweb\declaracion_volumen_interactivo.js"
    template_path = r"c:\simafiweb\venv\Scripts\tributario\tributario_app\templates\declaracion_volumen.html"
    js_destination = r"c:\simafiweb\venv\Scripts\tributario\tributario_app\static\js\declaracion_volumen_interactivo.js"
    
    # Verificar archivos
    if not os.path.exists(js_source):
        print(f"❌ Archivo JavaScript no encontrado: {js_source}")
        return False
        
    if not os.path.exists(template_path):
        print(f"❌ Template no encontrado: {template_path}")
        return False
    
    try:
        # Crear directorio static/js si no existe
        js_dir = os.path.dirname(js_destination)
        os.makedirs(js_dir, exist_ok=True)
        
        # Copiar JavaScript
        shutil.copy2(js_source, js_destination)
        print(f"✅ JavaScript copiado a: {js_destination}")
        
        # Leer template actual
        with open(template_path, 'r', encoding='utf-8') as f:
            contenido_template = f.read()
        
        # Crear backup
        backup_path = template_path + ".backup_calculadora"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(contenido_template)
        print(f"✅ Backup creado: {backup_path}")
        
        # Verificar si ya está integrado
        if 'declaracion_volumen_interactivo.js' in contenido_template:
            print("⚠️  La calculadora ya está integrada en el template")
            return True
        
        # Integrar JavaScript en el template
        js_include = '''
    <!-- Calculadora Interactiva ICS -->
    <script src="{% static 'js/declaracion_volumen_interactivo.js' %}"></script>
    <style>
        .campo-calculado {
            border-left: 3px solid #28a745 !important;
            background-color: #f8fff8 !important;
        }
        .resultado-calculo {
            background-color: #e8f5e8 !important;
            font-weight: bold;
            color: #155724;
        }
        .feedback-calculo {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #28a745;
            color: white;
            padding: 10px 15px;
            border-radius: 5px;
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
    </style>'''
        
        # Buscar donde insertar el JavaScript
        if '</body>' in contenido_template:
            contenido_modificado = contenido_template.replace('</body>', js_include + '\n</body>')
        elif '{% endblock %}' in contenido_template:
            contenido_modificado = contenido_template.replace('{% endblock %}', js_include + '\n{% endblock %}')
        else:
            # Agregar al final
            contenido_modificado = contenido_template + js_include
        
        # Agregar clases CSS a campos relevantes si no existen
        modificaciones_campos = [
            {
                'buscar': 'name="ventai"',
                'agregar_clase': 'campo-calculado'
            },
            {
                'buscar': 'name="ventac"', 
                'agregar_clase': 'campo-calculado'
            },
            {
                'buscar': 'name="ventas"',
                'agregar_clase': 'campo-calculado'
            },
            {
                'buscar': 'name="ventap"',
                'agregar_clase': 'campo-calculado'
            },
            {
                'buscar': 'id="id_impuesto',
                'agregar_clase': 'resultado-calculo'
            }
        ]
        
        for mod in modificaciones_campos:
            if mod['buscar'] in contenido_modificado:
                # Buscar el input y agregar clase si no existe
                import re
                pattern = f'(<input[^>]*{re.escape(mod["buscar"])}[^>]*)'
                matches = re.findall(pattern, contenido_modificado)
                for match in matches:
                    if 'class=' in match:
                        if mod['agregar_clase'] not in match:
                            nuevo_match = match.replace('class="', f'class="{mod["agregar_clase"]} ')
                            contenido_modificado = contenido_modificado.replace(match, nuevo_match)
                    else:
                        nuevo_match = match.replace('>', f' class="{mod["agregar_clase"]}">')
                        contenido_modificado = contenido_modificado.replace(match, nuevo_match)
        
        # Escribir template modificado
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(contenido_modificado)
        
        print("✅ Template declaracion_volumen.html modificado exitosamente")
        print("\n📋 FUNCIONALIDADES AGREGADAS:")
        print("   🔄 Cálculo automático al escribir en campos de ventas")
        print("   💰 Actualización automática del impuesto calculado")
        print("   🎨 Indicadores visuales en campos con cálculo")
        print("   ⚡ Feedback en tiempo real")
        print("   📊 Validación de formulario mejorada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la integración: {e}")
        return False

def mostrar_instrucciones():
    """
    Muestra instrucciones para usar la calculadora integrada
    """
    print("\n🚀 INSTRUCCIONES DE USO")
    print("=" * 30)
    print("1. Acceda al formulario declaración volumen")
    print("2. Los campos de ventas tendrán borde verde (cálculo automático)")
    print("3. Al escribir valores, el impuesto se calcula automáticamente")
    print("4. El resultado aparece en el campo 'impuesto calculado'")
    print("5. Feedback visual aparece en la esquina superior derecha")
    print("\n📝 CAMPOS CON CÁLCULO AUTOMÁTICO:")
    print("   • Ventas Industria (ventai)")
    print("   • Ventas Comercio (ventac)")
    print("   • Ventas Servicios (ventas)")
    print("   • Ventas Rubro Producción (ventap)")

if __name__ == "__main__":
    exito = integrar_calculadora_declaracion()
    
    if exito:
        print("\n🎉 INTEGRACIÓN COMPLETADA")
        mostrar_instrucciones()
        print("\n🔄 Reinicie el servidor Django para aplicar cambios")
    else:
        print("\n❌ INTEGRACIÓN FALLÓ")
        print("   Verifique los archivos y rutas mencionadas")
    
    print("\n" + "=" * 50)
