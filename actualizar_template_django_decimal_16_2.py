#!/usr/bin/env python
"""
Actualiza el template Django real para DECIMAL(16,2)
"""

import os
import re
import shutil

def actualizar_template_django():
    """
    Actualiza el template Django declaracion_volumen.html para DECIMAL(16,2)
    """
    print("🔧 ACTUALIZANDO TEMPLATE DJANGO DECIMAL(16,2)")
    print("=" * 50)
    
    template_path = r'C:\simafiweb\venv\Scripts\tributario\tributario_app\templates\declaracion_volumen.html'
    
    if not os.path.exists(template_path):
        print(f"❌ Template no encontrado: {template_path}")
        return False
    
    try:
        # Leer template
        with open(template_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Crear backup
        backup_path = template_path + ".backup_etiquetas_16_2"
        shutil.copy2(template_path, backup_path)
        print(f"✅ Backup creado: {os.path.basename(backup_path)}")
        
        # Actualizar campos de ventas
        campos_actualizaciones = {
            # Ventas Industria
            'name="ventai"': {
                'maxlength': '18',
                'pattern': r'^\d{1,14}(\.\d{0,2})?$',
                'title': 'DECIMAL(16,2): Máximo 14 enteros + 2 decimales',
                'placeholder': 'Ej: 12345678901234.56',
                'inputmode': 'decimal',
                'data-format': 'decimal-16-2'
            },
            # Ventas Comercio
            'name="ventac"': {
                'maxlength': '18',
                'pattern': r'^\d{1,14}(\.\d{0,2})?$',
                'title': 'DECIMAL(16,2): Máximo 14 enteros + 2 decimales',
                'placeholder': 'Ej: 98765432109876.54',
                'inputmode': 'decimal',
                'data-format': 'decimal-16-2'
            },
            # Ventas Servicios
            'name="ventas"': {
                'maxlength': '18',
                'pattern': r'^\d{1,14}(\.\d{0,2})?$',
                'title': 'DECIMAL(16,2): Máximo 14 enteros + 2 decimales',
                'placeholder': 'Ej: 55555555555555.55',
                'inputmode': 'decimal',
                'data-format': 'decimal-16-2'
            },
            # Ventas Rubro Producción
            'name="ventap"': {
                'maxlength': '18',
                'pattern': r'^\d{1,14}(\.\d{0,2})?$',
                'title': 'DECIMAL(16,2): Máximo 14 enteros + 2 decimales',
                'placeholder': 'Ej: 88888888888888.88',
                'inputmode': 'decimal',
                'data-format': 'decimal-16-2'
            }
        }
        
        # Aplicar actualizaciones
        for campo_name, atributos in campos_actualizaciones.items():
            # Buscar input con este name
            patron_input = f'(<input[^>]*{campo_name}[^>]*)'
            
            def actualizar_input(match):
                input_tag = match.group(1)
                
                for attr, valor in atributos.items():
                    if f'{attr}=' not in input_tag:
                        # Agregar atributo
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
        
        # Actualizar labels si existen
        labels_actualizaciones = {
            'Ventas Industria': 'Ventas Industria (DECIMAL 16,2)',
            'Ventas Comercio': 'Ventas Comercio (DECIMAL 16,2)', 
            'Ventas Servicios': 'Ventas Servicios (DECIMAL 16,2)',
            'Ventas Rubro Producción': 'Ventas Rubro Producción (DECIMAL 16,2)'
        }
        
        for label_viejo, label_nuevo in labels_actualizaciones.items():
            # Buscar en diferentes formatos
            patrones = [
                f'>{label_viejo}<',
                f'"{label_viejo}"',
                f"'{label_viejo}'"
            ]
            
            for patron in patrones:
                if patron in contenido and label_nuevo not in contenido:
                    contenido = contenido.replace(patron, patron.replace(label_viejo, label_nuevo))
        
        # Agregar comentario de especificación
        comentario_spec = '''
<!-- Campos de ventas configurados para DECIMAL(16,2) -->
<!-- Máximo: 14 enteros + 2 decimales = 99,999,999,999,999.99 -->
<!-- Actualizado para soportar volúmenes de ventas grandes -->
'''
        
        # Insertar comentario antes del primer campo de ventas
        if 'name="ventai"' in contenido and '<!-- Campos de ventas configurados' not in contenido:
            contenido = contenido.replace(
                'name="ventai"',
                comentario_spec + 'name="ventai"',
                1
            )
        
        # Escribir template actualizado
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        print("✅ Template Django actualizado exitosamente")
        print("   • Campos configurados para DECIMAL(16,2)")
        print("   • Atributos HTML actualizados")
        print("   • Labels mejorados con especificación")
        print("   • Placeholders con ejemplos de 14 dígitos")
        
        return True
        
    except Exception as e:
        print(f"❌ Error actualizando template: {e}")
        return False

def verificar_actualizacion():
    """
    Verifica que la actualización se aplicó correctamente
    """
    print("\n🔍 VERIFICANDO ACTUALIZACIÓN")
    print("=" * 30)
    
    template_path = r'C:\simafiweb\venv\Scripts\tributario\tributario_app\templates\declaracion_volumen.html'
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        verificaciones = [
            ('maxlength="18"', 'Longitud máxima configurada'),
            ('pattern="^\\d{1,14}', 'Patrón DECIMAL(16,2) aplicado'),
            ('DECIMAL(16,2)', 'Especificación en labels'),
            ('data-format="decimal-16-2"', 'Atributo de formato agregado'),
            ('inputmode="decimal"', 'Modo de entrada decimal')
        ]
        
        for buscar, descripcion in verificaciones:
            if buscar in contenido:
                print(f"   ✅ {descripcion}")
            else:
                print(f"   ⚠️  {descripcion} - No encontrado")
        
        # Contar campos actualizados
        campos_actualizados = contenido.count('data-format="decimal-16-2"')
        print(f"\n📊 Campos actualizados: {campos_actualizados}/4")
        
        if campos_actualizados == 4:
            print("✅ Todos los campos de ventas actualizados correctamente")
        else:
            print("⚠️  Algunos campos pueden necesitar revisión manual")
            
    except Exception as e:
        print(f"❌ Error en verificación: {e}")

def mostrar_resumen():
    """
    Muestra resumen de la actualización
    """
    print("\n🎉 TEMPLATE DJANGO ACTUALIZADO PARA DECIMAL(16,2)")
    print("=" * 55)
    print("📊 ESPECIFICACIONES APLICADAS:")
    print("   • Formato: DECIMAL(16,2)")
    print("   • Enteros: Máximo 14 dígitos")
    print("   • Decimales: Máximo 2 dígitos")
    print("   • Valor máximo: 99,999,999,999,999.99")
    print()
    print("✅ ATRIBUTOS HTML ACTUALIZADOS:")
    print("   • maxlength='18' (14+1+2+1 buffer)")
    print("   • pattern='^\\d{1,14}(\\.\\d{0,2})?$'")
    print("   • title='DECIMAL(16,2): Máximo 14 enteros + 2 decimales'")
    print("   • inputmode='decimal'")
    print("   • data-format='decimal-16-2'")
    print()
    print("🎯 CAMPOS ACTUALIZADOS:")
    print("   • Ventas Industria (ventai)")
    print("   • Ventas Comercio (ventac)")
    print("   • Ventas Servicios (ventas)")
    print("   • Ventas Rubro Producción (ventap)")
    print()
    print("📝 MEJORAS APLICADAS:")
    print("   • Labels incluyen especificación DECIMAL(16,2)")
    print("   • Placeholders con ejemplos de 14 dígitos")
    print("   • Comentarios de documentación agregados")
    print("   • Validación HTML nativa habilitada")

if __name__ == "__main__":
    print("🎯 ACTUALIZACIÓN TEMPLATE DJANGO")
    print("   Configurando para DECIMAL(16,2)")
    print("   14 enteros + 2 decimales")
    print()
    
    if actualizar_template_django():
        verificar_actualizacion()
        mostrar_resumen()
        
        print("\n🔄 REINICIE EL SERVIDOR DJANGO PARA VER CAMBIOS")
        print("=" * 50)
    else:
        print("\n❌ La actualización falló")
        print("   Revise los errores y ejecute nuevamente")
