#!/usr/bin/env python
"""
Actualiza las etiquetas y atributos del formulario para DECIMAL(16,2)
14 enteros + 2 decimales
"""

import os
import re

def actualizar_etiquetas_formulario():
    """
    Actualiza etiquetas y atributos de campos de ventas para DECIMAL(16,2)
    """
    print("🔧 ACTUALIZANDO ETIQUETAS FORMULARIO DECIMAL(16,2)")
    print("=" * 50)
    print("Formato: 14 enteros + 2 decimales")
    print("Máximo: 99,999,999,999,999.99")
    print()
    
    # Archivos a actualizar
    archivos = [
        {
            'path': 'test_calculo_automatico.html',
            'tipo': 'test'
        },
        {
            'path': r'C:\simafiweb\venv\Scripts\tributario\tributario_app\templates\declaracion_volumen.html',
            'tipo': 'django'
        }
    ]
    
    for archivo_info in archivos:
        archivo_path = archivo_info['path']
        tipo = archivo_info['tipo']
        
        if not os.path.exists(archivo_path):
            print(f"⚠️  Archivo no encontrado: {archivo_path}")
            continue
            
        print(f"📝 Actualizando {tipo}: {os.path.basename(archivo_path)}")
        
        try:
            # Leer archivo
            with open(archivo_path, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Crear backup
            backup_path = archivo_path + ".backup_etiquetas"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(contenido)
            print(f"   ✅ Backup: {os.path.basename(backup_path)}")
            
            # Actualizar según tipo
            if tipo == 'test':
                contenido = actualizar_formulario_test(contenido)
            elif tipo == 'django':
                contenido = actualizar_formulario_django(contenido)
            
            # Escribir archivo actualizado
            with open(archivo_path, 'w', encoding='utf-8') as f:
                f.write(contenido)
            
            print(f"   ✅ Actualizado exitosamente")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")

def actualizar_formulario_test(contenido):
    """
    Actualiza el formulario de test
    """
    # Actualizar atributos de inputs de ventas
    campos_ventas = [
        ('id_ventai', 'Ventas Industria'),
        ('id_ventac', 'Ventas Comercio'),
        ('id_ventas', 'Ventas Servicios'),
        ('id_ventap', 'Ventas Rubro Producción')
    ]
    
    for campo_id, label in campos_ventas:
        # Buscar y actualizar input
        patron_input = f'(<input[^>]*id="{campo_id}"[^>]*)'
        
        def actualizar_input(match):
            input_tag = match.group(1)
            
            # Actualizar/agregar atributos
            atributos = {
                'maxlength': '18',  # 14 enteros + 1 punto + 2 decimales + 1 buffer
                'pattern': r'^\d{1,14}(\.\d{0,2})?$',
                'title': 'Formato DECIMAL(16,2): Máximo 14 enteros + 2 decimales',
                'step': '0.01',
                'inputmode': 'decimal'
            }
            
            for attr, valor in atributos.items():
                if f'{attr}=' not in input_tag:
                    input_tag = input_tag.rstrip('>') + f' {attr}="{valor}"'
                else:
                    # Reemplazar valor existente
                    input_tag = re.sub(
                        f'{attr}="[^"]*"',
                        f'{attr}="{valor}"',
                        input_tag
                    )
            
            return input_tag + '>'
        
        contenido = re.sub(patron_input, actualizar_input, contenido)
    
    # Actualizar placeholders con ejemplos de 14 dígitos
    placeholders_nuevos = {
        'placeholder="Ej: 12345678901234.56"': 'placeholder="Ej: 12345678901234.56"',
        'placeholder="Ej: 98765432109876.54"': 'placeholder="Ej: 98765432109876.54"',
        'placeholder="Ej: 55555555555555.55"': 'placeholder="Ej: 55555555555555.55"',
        'placeholder="Ej: 88888888888888.88"': 'placeholder="Ej: 88888888888888.88"'
    }
    
    for viejo, nuevo in placeholders_nuevos.items():
        contenido = contenido.replace(viejo, nuevo)
    
    # Actualizar información de formato en la página
    contenido = contenido.replace(
        '• Máximo: 16 enteros + 2 decimales',
        '• Máximo: 14 enteros + 2 decimales'
    )
    contenido = contenido.replace(
        '• Ejemplo: 9,999,999,999,999,999.99',
        '• Ejemplo: 99,999,999,999,999.99'
    )
    
    # Actualizar labels para ser más descriptivos
    labels_mejorados = {
        '<label for="id_ventai" class="form-label">Ventas Industria</label>': 
        '<label for="id_ventai" class="form-label">Ventas Industria <small class="text-muted">(DECIMAL 16,2)</small></label>',
        
        '<label for="id_ventac" class="form-label">Ventas Comercio</label>':
        '<label for="id_ventac" class="form-label">Ventas Comercio <small class="text-muted">(DECIMAL 16,2)</small></label>',
        
        '<label for="id_ventas" class="form-label">Ventas Servicios</label>':
        '<label for="id_ventas" class="form-label">Ventas Servicios <small class="text-muted">(DECIMAL 16,2)</small></label>',
        
        '<label for="id_ventap" class="form-label"><strong>Ventas Rubro Producción</strong></label>':
        '<label for="id_ventap" class="form-label"><strong>Ventas Rubro Producción</strong> <small class="text-success">(DECIMAL 16,2)</small></label>'
    }
    
    for viejo, nuevo in labels_mejorados.items():
        contenido = contenido.replace(viejo, nuevo)
    
    return contenido

def actualizar_formulario_django(contenido):
    """
    Actualiza el formulario Django real
    """
    # Buscar y actualizar campos de ventas en Django
    campos_ventas = ['ventai', 'ventac', 'ventas', 'ventap']
    
    for campo in campos_ventas:
        # Actualizar inputs por name
        patron_input = f'(<input[^>]*name="{campo}"[^>]*)'
        
        def actualizar_input_django(match):
            input_tag = match.group(1)
            
            # Atributos para DECIMAL(16,2)
            atributos = {
                'maxlength': '18',
                'pattern': r'^\d{1,14}(\.\d{0,2})?$',
                'title': 'DECIMAL(16,2): Máximo 14 enteros + 2 decimales',
                'step': '0.01',
                'inputmode': 'decimal',
                'data-format': 'decimal-16-2'
            }
            
            for attr, valor in atributos.items():
                if f'{attr}=' not in input_tag:
                    input_tag = input_tag.rstrip('>') + f' {attr}="{valor}"'
                else:
                    # Reemplazar valor existente
                    input_tag = re.sub(
                        f'{attr}="[^"]*"',
                        f'{attr}="{valor}"',
                        input_tag
                    )
            
            return input_tag + '>'
        
        contenido = re.sub(patron_input, actualizar_input_django, contenido)
    
    # Actualizar labels en Django si existen
    labels_django = {
        'Ventas Industria': 'Ventas Industria (DECIMAL 16,2)',
        'Ventas Comercio': 'Ventas Comercio (DECIMAL 16,2)',
        'Ventas Servicios': 'Ventas Servicios (DECIMAL 16,2)',
        'Ventas Rubro Producción': 'Ventas Rubro Producción (DECIMAL 16,2)'
    }
    
    for viejo, nuevo in labels_django.items():
        # Buscar labels en diferentes formatos Django
        patrones_label = [
            f'>{viejo}<',
            f'"{viejo}"',
            f"'{viejo}'"
        ]
        
        for patron in patrones_label:
            contenido = contenido.replace(patron, patron.replace(viejo, nuevo))
    
    # Agregar comentario de especificación
    comentario_spec = '''
<!-- Campos de ventas configurados para DECIMAL(16,2) -->
<!-- Máximo: 14 enteros + 2 decimales = 99,999,999,999,999.99 -->
'''
    
    # Insertar comentario antes del primer campo de ventas
    if 'name="ventai"' in contenido and '<!-- Campos de ventas configurados' not in contenido:
        contenido = contenido.replace(
            'name="ventai"',
            comentario_spec + 'name="ventai"',
            1
        )
    
    return contenido

def agregar_validacion_css():
    """
    Agrega CSS para validación visual
    """
    css_validacion = '''
<style>
/* Validación visual para DECIMAL(16,2) */
input[data-format="decimal-16-2"]:invalid {
    border-color: #dc3545 !important;
    box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25) !important;
}

input[data-format="decimal-16-2"]:valid {
    border-color: #28a745 !important;
}

.decimal-16-2-info {
    font-size: 0.875em;
    color: #6c757d;
    margin-top: 0.25rem;
}

.decimal-16-2-info::before {
    content: "💡 ";
}
</style>'''
    
    return css_validacion

def mostrar_resumen_actualizacion():
    """
    Muestra resumen de la actualización
    """
    print("\n🎉 ETIQUETAS FORMULARIO ACTUALIZADAS")
    print("=" * 45)
    print("📊 ESPECIFICACIONES APLICADAS:")
    print("   • Formato: DECIMAL(16,2)")
    print("   • Enteros: Máximo 14 dígitos")
    print("   • Decimales: Máximo 2 dígitos")
    print("   • Valor máximo: 99,999,999,999,999.99")
    print()
    print("✅ ATRIBUTOS ACTUALIZADOS:")
    print("   • maxlength='18' (14+1+2+1 buffer)")
    print("   • pattern='^\\d{1,14}(\\.\\d{0,2})?$'")
    print("   • title='Formato DECIMAL(16,2)'")
    print("   • step='0.01'")
    print("   • inputmode='decimal'")
    print()
    print("🎯 CAMPOS ACTUALIZADOS:")
    print("   • Ventas Industria (ventai)")
    print("   • Ventas Comercio (ventac)")
    print("   • Ventas Servicios (ventas)")
    print("   • Ventas Rubro Producción (ventap)")
    print()
    print("📝 LABELS MEJORADOS:")
    print("   • Incluyen especificación DECIMAL(16,2)")
    print("   • Ejemplos actualizados a 14 dígitos")
    print("   • Información de formato visible")

if __name__ == "__main__":
    print("🎯 ACTUALIZACIÓN ETIQUETAS FORMULARIO")
    print("   Configurando para DECIMAL(16,2)")
    print("   14 enteros + 2 decimales")
    print()
    
    actualizar_etiquetas_formulario()
    mostrar_resumen_actualizacion()
    
    print("\n🔄 REINICIE EL SERVIDOR PARA VER CAMBIOS")
    print("=" * 45)
