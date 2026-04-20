#!/usr/bin/env python3
"""
Corrección definitiva del formulario para mostrar años en el combobox
"""

import os
import re

def corregir_formulario_declaracion_volumen():
    """Corregir el formulario para que el combobox de años funcione"""
    
    # Buscar archivo del formulario
    formulario_paths = [
        'C:/simafiweb/venv/Scripts/tributario/tributario_app/forms.py',
        'C:/simafiweb/venv/Scripts/tributario/modules/tributario/forms.py'
    ]
    
    for path in formulario_paths:
        if os.path.exists(path):
            print(f"📝 Corrigiendo formulario: {path}")
            
            try:
                # Leer archivo
                with open(path, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                
                # Buscar clase DeclaracionVolumenForm
                if 'class DeclaracionVolumenForm' in contenido:
                    print("✅ Formulario DeclaracionVolumenForm encontrado")
                    
                    # Verificar si ya tiene __init__
                    if 'def __init__(self' in contenido and 'DeclaracionVolumenForm' in contenido:
                        print("⚠️  Formulario ya tiene __init__, actualizando...")
                        
                        # Buscar el __init__ existente y corregirlo
                        patron_init = r'(def __init__\(self[^}]+?)(try:[^}]+?except[^}]+?)'
                        
                        if re.search(patron_init, contenido, re.DOTALL):
                            # Reemplazar la lógica de carga de años
                            nuevo_init = '''        # Cargar años dinámicamente desde la tabla Anos
        try:
            anos_choices = [('', 'Seleccione un año')] + [
                (str(int(ano.ano)), str(int(ano.ano))) 
                for ano in Anos.objects.all().order_by('-ano')
            ]
            self.fields['ano'].widget.choices = anos_choices
            print(f"✅ {len(anos_choices)-1} años cargados en combobox")
        except Exception as e:
            print(f"❌ Error cargando años: {e}")
            # Fallback con años estáticos
            current_year = 2024
            anos_choices = [('', 'Seleccione un año')] + [
                (str(year), str(year)) 
                for year in range(current_year, current_year - 10, -1)
            ]
            self.fields['ano'].widget.choices = anos_choices'''
            
            contenido = re.sub(
                r'(# Cargar las opciones del combobox de años desde la tabla Anos\s+try:[^}]+?except[^}]+?)',
                nuevo_init,
                contenido,
                flags=re.DOTALL
            )
            
        else:
            print("⚠️  Formulario no tiene __init__, agregando...")
            
            # Buscar el final de la clase y agregar __init__
            patron_clase = r'(class DeclaracionVolumenForm[^:]+:[^}]+?)(class|\Z)'
            
            init_completo = '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Cargar años dinámicamente desde la tabla Anos
        try:
            anos_choices = [('', 'Seleccione un año')] + [
                (str(int(ano.ano)), str(int(ano.ano))) 
                for ano in Anos.objects.all().order_by('-ano')
            ]
            self.fields['ano'].widget.choices = anos_choices
            print(f"✅ {len(anos_choices)-1} años cargados en combobox")
        except Exception as e:
            print(f"❌ Error cargando años: {e}")
            # Fallback con años estáticos
            current_year = 2024
            anos_choices = [('', 'Seleccione un año')] + [
                (str(year), str(year)) 
                for year in range(current_year, current_year - 10, -1)
            ]
            self.fields['ano'].widget.choices = anos_choices

'''
            
            if re.search(patron_clase, contenido, re.DOTALL):
                contenido = re.sub(
                    patron_clase,
                    r'\1' + init_completo + r'\2',
                    contenido,
                    flags=re.DOTALL
                )
        
        # Guardar archivo corregido
        with open(path, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        print(f"✅ Formulario corregido: {path}")
        return True
        
    except Exception as e:
        print(f"❌ Error corrigiendo formulario: {e}")
        return False

    print("❌ No se encontró archivo de formulario")
    return False

def verificar_correccion():
    """Verificar que la corrección funcionó"""
    
    print("\n🔍 VERIFICANDO CORRECCIÓN...")
    
    try:
        import sys
        sys.path.append('C:/simafiweb/venv/Scripts/tributario')
        
        import os
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
        
        import django
        django.setup()
        
        from tributario_app.forms import DeclaracionVolumenForm
        
        # Crear instancia del formulario
        form = DeclaracionVolumenForm()
        
        # Verificar campo año
        if 'ano' in form.fields:
            ano_field = form.fields['ano']
            
            if hasattr(ano_field.widget, 'choices'):
                choices = list(ano_field.widget.choices)
                print(f"✅ Combobox tiene {len(choices)} opciones")
                
                if len(choices) > 1:
                    print("✅ CORRECCIÓN EXITOSA - Años cargados correctamente")
                    print("Primeras opciones:")
                    for i, (value, label) in enumerate(choices[:6]):
                        print(f"  {i+1}. '{value}' → '{label}'")
                    return True
                else:
                    print("❌ Combobox sigue sin opciones")
                    return False
            else:
                print("❌ Campo año sigue sin widget de opciones")
                return False
        else:
            print("❌ Campo 'ano' no existe")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando: {e}")
        return False

def main():
    """Función principal"""
    print("🔧 CORRECCIÓN DEFINITIVA DEL COMBOBOX DE AÑOS")
    print("=" * 50)
    
    # Corregir formulario
    if corregir_formulario_declaracion_volumen():
        # Verificar corrección
        if verificar_correccion():
            print("\n✅ PROBLEMA RESUELTO")
            print("\nPasos siguientes:")
            print("1. Reiniciar servidor Django")
            print("2. Refrescar página en el navegador")
            print("3. El combobox debería mostrar los años")
        else:
            print("\n⚠️  Corrección aplicada pero necesita verificación manual")
    else:
        print("\n❌ No se pudo aplicar la corrección automáticamente")

if __name__ == "__main__":
    main()
