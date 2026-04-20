#!/usr/bin/env python3
"""
Solución directa para el problema del combobox de años
"""

import os
import sys
import django

# Configurar Django
sys.path.append('C:/simafiweb/venv/Scripts/tributario')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')

def aplicar_solucion():
    """Aplicar la solución directa al formulario"""
    
    print("🔧 APLICANDO SOLUCIÓN AL COMBOBOX DE AÑOS")
    print("=" * 50)
    
    # Configurar Django
    try:
        django.setup()
        print("✅ Django configurado")
    except Exception as e:
        print(f"❌ Error Django: {e}")
        return False
    
    # Buscar y corregir el archivo forms.py
    forms_path = 'C:/simafiweb/venv/Scripts/tributario/tributario_app/forms.py'
    
    if not os.path.exists(forms_path):
        print(f"❌ Archivo no encontrado: {forms_path}")
        return False
    
    print(f"📝 Procesando: {forms_path}")
    
    try:
        # Leer archivo
        with open(forms_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Verificar si DeclaracionVolumenForm existe
        if 'class DeclaracionVolumenForm' not in contenido:
            print("❌ DeclaracionVolumenForm no encontrado")
            return False
        
        print("✅ DeclaracionVolumenForm encontrado")
        
        # Buscar el __init__ existente
        if 'def __init__(self, *args, **kwargs):' in contenido:
            print("✅ __init__ existente encontrado")
            
            # Buscar la sección de años y reemplazarla
            patron_anos = r'(# Cargar las opciones del combobox de años desde la tabla Anos\s+try:.*?except.*?self\.fields\[\'ano\'\]\.widget\.choices = anos_choices)'
            
            nuevo_codigo_anos = '''        # Cargar las opciones del combobox de años desde la tabla Anos
        try:
            anos_choices = [('', 'Seleccione un año')]
            for ano in Anos.objects.all().order_by('-ano'):
                valor_ano = str(int(ano.ano))
                anos_choices.append((valor_ano, valor_ano))
            
            # Asignar opciones al widget
            if 'ano' in self.fields:
                self.fields['ano'].widget.choices = anos_choices
                print(f"✅ {len(anos_choices)-1} años cargados en combobox")
            
        except Exception as e:
            print(f"❌ Error cargando años: {e}")
            # Fallback con años estáticos
            anos_choices = [('', 'Seleccione un año')]
            for year in range(2024, 2014, -1):
                anos_choices.append((str(year), str(year)))
            
            if 'ano' in self.fields:
                self.fields['ano'].widget.choices = anos_choices'''
            
            import re
            contenido_nuevo = re.sub(
                patron_anos,
                nuevo_codigo_anos,
                contenido,
                flags=re.DOTALL
            )
            
            if contenido_nuevo != contenido:
                print("✅ Código de años actualizado")
            else:
                print("⚠️  No se pudo actualizar automáticamente, aplicando manualmente...")
                
                # Buscar donde insertar el código
                if 'self.fields[\'ano\'].widget.choices = anos_choices' in contenido:
                    # Reemplazar toda la sección try-except
                    contenido_nuevo = re.sub(
                        r'try:\s+anos_choices.*?self\.fields\[\'ano\'\]\.widget\.choices = anos_choices',
                        nuevo_codigo_anos.strip(),
                        contenido,
                        flags=re.DOTALL
                    )
        else:
            print("⚠️  __init__ no encontrado, agregando completo...")
            
            # Buscar el final de la clase DeclaracionVolumenForm
            patron_clase = r'(class DeclaracionVolumenForm.*?\n)(class|\Z)'
            
            init_completo = '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Cargar las opciones del combobox de años desde la tabla Anos
        try:
            anos_choices = [('', 'Seleccione un año')]
            for ano in Anos.objects.all().order_by('-ano'):
                valor_ano = str(int(ano.ano))
                anos_choices.append((valor_ano, valor_ano))
            
            # Asignar opciones al widget
            if 'ano' in self.fields:
                self.fields['ano'].widget.choices = anos_choices
                print(f"✅ {len(anos_choices)-1} años cargados en combobox")
            
        except Exception as e:
            print(f"❌ Error cargando años: {e}")
            # Fallback con años estáticos
            anos_choices = [('', 'Seleccione un año')]
            for year in range(2024, 2014, -1):
                anos_choices.append((str(year), str(year)))
            
            if 'ano' in self.fields:
                self.fields['ano'].widget.choices = anos_choices

'''
            
            contenido_nuevo = re.sub(
                patron_clase,
                r'\1' + init_completo + r'\2',
                contenido,
                flags=re.DOTALL
            )
        
        # Guardar archivo
        with open(forms_path, 'w', encoding='utf-8') as f:
            f.write(contenido_nuevo)
        
        print("✅ Archivo forms.py actualizado")
        return True
        
    except Exception as e:
        print(f"❌ Error procesando archivo: {e}")
        return False

def verificar_solucion():
    """Verificar que la solución funciona"""
    
    print("\n🔍 VERIFICANDO SOLUCIÓN...")
    
    try:
        from tributario_app.forms import DeclaracionVolumenForm
        
        # Crear instancia del formulario
        form = DeclaracionVolumenForm()
        
        # Verificar campo año
        if 'ano' in form.fields:
            ano_field = form.fields['ano']
            
            if hasattr(ano_field.widget, 'choices'):
                choices = list(ano_field.widget.choices)
                print(f"✅ Combobox configurado con {len(choices)} opciones")
                
                if len(choices) > 1:
                    print("✅ SOLUCIÓN EXITOSA")
                    print("Opciones disponibles:")
                    for i, (value, label) in enumerate(choices[:8]):
                        print(f"  {i+1}. '{value}' → '{label}'")
                    return True
                else:
                    print("❌ Combobox sigue vacío")
                    return False
            else:
                print("❌ Widget no configurado")
                return False
        else:
            print("❌ Campo 'ano' no existe")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando: {e}")
        return False

def main():
    """Función principal"""
    
    if aplicar_solucion():
        if verificar_solucion():
            print("\n🎉 PROBLEMA RESUELTO EXITOSAMENTE")
            print("\nEl combobox de años ahora debería mostrar:")
            print("- Opción vacía 'Seleccione un año'")
            print("- Todos los años de la tabla 'anos' ordenados descendente")
            print("\n📋 Pasos finales:")
            print("1. Reiniciar servidor Django")
            print("2. Refrescar navegador (Ctrl+F5)")
            print("3. Verificar que el combobox muestra los años")
        else:
            print("\n⚠️  Solución aplicada, verificar manualmente")
    else:
        print("\n❌ No se pudo aplicar la solución automáticamente")

if __name__ == "__main__":
    main()
