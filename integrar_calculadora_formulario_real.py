#!/usr/bin/env python
"""
Integra la calculadora automática en el formulario real declaracion_volumen
"""

import os
import shutil

def integrar_calculadora_formulario_real():
    """
    Integra la calculadora en el formulario real de declaracion_volumen
    """
    print("🔧 INTEGRANDO CALCULADORA EN FORMULARIO REAL")
    print("=" * 50)
    
    # Rutas de archivos
    js_source = r"c:\simafiweb\declaracion_volumen_interactivo.js"
    template_path = r"C:\simafiweb\venv\Scripts\tributario\tributario_app\templates\declaracion_volumen.html"
    js_destination = r"C:\simafiweb\venv\Scripts\tributario\tributario_app\static\js\declaracion_volumen_interactivo.js"
    
    print("📁 RUTAS DE INTEGRACIÓN:")
    print(f"   JavaScript origen: {js_source}")
    print(f"   Template destino: {template_path}")
    print(f"   JavaScript destino: {js_destination}")
    print()
    
    # Verificar archivos
    if not os.path.exists(js_source):
        print(f"❌ JavaScript no encontrado: {js_source}")
        return False
        
    if not os.path.exists(template_path):
        print(f"❌ Template no encontrado: {template_path}")
        print("   Verifique la ruta del template declaracion_volumen.html")
        return False
    
    try:
        # Crear directorio static/js si no existe
        js_dir = os.path.dirname(js_destination)
        os.makedirs(js_dir, exist_ok=True)
        print(f"✅ Directorio creado/verificado: {js_dir}")
        
        # Copiar JavaScript
        shutil.copy2(js_source, js_destination)
        print(f"✅ JavaScript copiado a: {js_destination}")
        
        # Leer template actual
        with open(template_path, 'r', encoding='utf-8') as f:
            contenido_template = f.read()
        
        # Crear backup
        backup_path = template_path + ".backup_calculadora_real"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(contenido_template)
        print(f"✅ Backup creado: {backup_path}")
        
        # Verificar si ya está integrado
        if 'declaracion_volumen_interactivo.js' in contenido_template:
            print("⚠️  La calculadora ya está integrada en el template")
            return True
        
        # Integrar JavaScript y CSS en el template
        integracion_codigo = '''
<!-- Calculadora Automática ICS - Integración Real -->
{% load static %}
<script src="{% static 'js/declaracion_volumen_interactivo.js' %}"></script>
<style>
    /* Estilos para calculadora automática */
    .campo-calculado {
        border-left: 4px solid #28a745 !important;
        background-color: #f8fff8 !important;
        transition: all 0.3s ease;
    }
    
    .campo-calculado:focus {
        box-shadow: 0 0 0 0.2rem rgba(40, 167, 69, 0.25) !important;
        border-color: #28a745 !important;
    }
    
    .resultado-calculo {
        background-color: #e8f5e8 !important;
        font-weight: bold !important;
        color: #155724 !important;
        border: 2px solid #28a745 !important;
        font-size: 1.1em !important;
    }
    
    .feedback-calculo {
        position: fixed;
        top: 20px;
        right: 20px;
        background: #28a745;
        color: white;
        padding: 12px 18px;
        border-radius: 8px;
        z-index: 1050;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        font-weight: bold;
        min-width: 280px;
        animation: slideIn 0.3s ease;
    }
    
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .campo-ventas-destacado {
        background: linear-gradient(135deg, #f8fff8 0%, #e8f5e8 100%) !important;
        border: 2px solid #28a745 !important;
        font-weight: 500;
    }
    
    .indicador-calculo {
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        color: #28a745;
        font-weight: bold;
        font-size: 0.9em;
    }
</style>

<script>
// Configuración específica para formulario real
document.addEventListener('DOMContentLoaded', function() {
    // Agregar indicadores visuales a campos de ventas
    const camposVentas = ['id_ventai', 'id_ventac', 'id_ventas', 'id_ventap'];
    
    camposVentas.forEach(campoId => {
        const campo = document.getElementById(campoId);
        if (campo) {
            campo.classList.add('campo-calculado');
            
            // Agregar indicador de cálculo automático
            const parent = campo.parentElement;
            if (parent && !parent.querySelector('.indicador-calculo')) {
                const indicador = document.createElement('span');
                indicador.className = 'indicador-calculo';
                indicador.innerHTML = '⚡ Auto';
                indicador.title = 'Cálculo automático activado';
                parent.style.position = 'relative';
                parent.appendChild(indicador);
            }
        }
    });
    
    // Destacar campo de impuesto
    const campoImpuesto = document.getElementById('id_impuesto');
    if (campoImpuesto) {
        campoImpuesto.classList.add('resultado-calculo');
        campoImpuesto.readOnly = true;
        campoImpuesto.title = 'Campo calculado automáticamente - Tabla declara';
    }
    
    // Mensaje de bienvenida
    setTimeout(() => {
        if (window.declaracionVolumenInteractivo) {
            mostrarNotificacion('🚀 Calculadora automática ICS activada');
        }
    }, 1000);
});

function mostrarNotificacion(mensaje) {
    const notif = document.createElement('div');
    notif.className = 'feedback-calculo';
    notif.innerHTML = mensaje;
    document.body.appendChild(notif);
    
    setTimeout(() => {
        if (notif && notif.parentNode) {
            notif.style.opacity = '0';
            setTimeout(() => notif.remove(), 300);
        }
    }, 4000);
}

// Función para recalcular manualmente (botón opcional)
function recalcularImpuestos() {
    if (window.declaracionVolumenInteractivo) {
        window.declaracionVolumenInteractivo.recalcular();
        mostrarNotificacion('🔄 Impuestos recalculados');
    }
}
</script>'''
        
        # Buscar donde insertar el código
        if '</head>' in contenido_template:
            contenido_modificado = contenido_template.replace('</head>', integracion_codigo + '\n</head>')
        elif '{% endblock %}' in contenido_template and 'head' in contenido_template:
            contenido_modificado = contenido_template.replace('{% endblock %}', integracion_codigo + '\n{% endblock %}', 1)
        elif '</body>' in contenido_template:
            contenido_modificado = contenido_template.replace('</body>', integracion_codigo + '\n</body>')
        else:
            # Agregar al final
            contenido_modificado = contenido_template + integracion_codigo
        
        # Agregar clases CSS a campos específicos si existen
        import re
        
        # Buscar y modificar campos de ventas
        campos_modificar = [
            ('name="ventai"', 'campo-calculado'),
            ('name="ventac"', 'campo-calculado'),
            ('name="ventas"', 'campo-calculado'),
            ('name="ventap"', 'campo-calculado campo-ventas-destacado'),
            ('name="impuesto"', 'resultado-calculo'),
            ('id="id_impuesto"', 'resultado-calculo')
        ]
        
        for patron, clase in campos_modificar:
            # Buscar inputs con el patrón
            regex_input = f'(<input[^>]*{re.escape(patron)}[^>]*)'
            matches = re.findall(regex_input, contenido_modificado)
            
            for match in matches:
                if 'class=' in match:
                    # Agregar clase a class existente
                    if clase not in match:
                        nuevo_match = re.sub(r'class="([^"]*)"', f'class="\\1 {clase}"', match)
                        contenido_modificado = contenido_modificado.replace(match, nuevo_match)
                else:
                    # Agregar atributo class
                    nuevo_match = match.replace('>', f' class="{clase}">')
                    contenido_modificado = contenido_modificado.replace(match, nuevo_match)
        
        # Escribir template modificado
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(contenido_modificado)
        
        print("✅ Template declaracion_volumen.html modificado exitosamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la integración: {e}")
        # Restaurar backup si existe
        if 'backup_path' in locals() and os.path.exists(backup_path):
            try:
                shutil.copy2(backup_path, template_path)
                print("🔄 Backup restaurado debido al error")
            except:
                pass
        return False

def mostrar_resumen_integracion():
    """
    Muestra resumen de la integración realizada
    """
    print("\n🎉 INTEGRACIÓN COMPLETADA EN FORMULARIO REAL")
    print("=" * 50)
    print("📋 FUNCIONALIDADES INTEGRADAS:")
    print("   ✅ Cálculo automático al escribir en campos de ventas")
    print("   ✅ Campo 'impuesto' mapeado a tabla 'declara'")
    print("   ✅ Indicadores visuales (bordes verdes)")
    print("   ✅ Notificaciones de cálculo en tiempo real")
    print("   ✅ Campo 'Ventas Rubro Producción' destacado")
    print("   ✅ Formateo automático con separadores de miles")
    print("   ✅ Validación de formulario mejorada")
    print()
    print("🎯 CAMPOS CON CÁLCULO AUTOMÁTICO:")
    print("   • Ventas Industria (ventai) - Borde verde")
    print("   • Ventas Comercio (ventac) - Borde verde")
    print("   • Ventas Servicios (ventas) - Borde verde")
    print("   • Ventas Rubro Producción (ventap) - Destacado")
    print("   • Impuesto Calculado - Campo resultado")
    print()
    print("🔄 PRÓXIMOS PASOS:")
    print("   1. Reinicie el servidor Django")
    print("   2. Acceda al formulario declaracion_volumen")
    print("   3. Ingrese valores en campos de ventas")
    print("   4. Verifique cálculo automático del impuesto")

if __name__ == "__main__":
    print("🚀 INTEGRACIÓN EN FORMULARIO REAL DECLARACION_VOLUMEN")
    print("   Integrando calculadora automática probada y funcional")
    print()
    
    exito = integrar_calculadora_formulario_real()
    
    if exito:
        mostrar_resumen_integracion()
    else:
        print("\n❌ INTEGRACIÓN FALLÓ")
        print("   Verifique las rutas y permisos de archivos")
        print("   Revise que el template declaracion_volumen.html exista")
    
    print("\n" + "=" * 50)
