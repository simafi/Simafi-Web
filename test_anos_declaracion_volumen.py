#!/usr/bin/env python3
"""
Test para verificar que el combobox de años funciona correctamente
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')

try:
    django.setup()
    from tributario_app.models import Anos
    from tributario_app.forms import DeclaracionVolumenForm
    print("✅ Django configurado correctamente")
except Exception as e:
    print(f"❌ Error configurando Django: {e}")
    sys.exit(1)

def test_modelo_anos():
    """Test del modelo Anos"""
    print("\n=== TEST MODELO ANOS ===")
    
    try:
        # Contar años
        total = Anos.objects.count()
        print(f"Total años en BD: {total}")
        
        if total > 0:
            # Obtener primer y último año
            primer_ano = Anos.objects.order_by('ano').first()
            ultimo_ano = Anos.objects.order_by('-ano').first()
            
            print(f"Rango de años: {int(primer_ano.ano)} - {int(ultimo_ano.ano)}")
            
            # Mostrar algunos años
            anos_sample = Anos.objects.all().order_by('-ano')[:5]
            print("Últimos 5 años:")
            for ano in anos_sample:
                print(f"  - {int(ano.ano)}")
        else:
            print("⚠️  No hay años en la base de datos")
            
        return total > 0
        
    except Exception as e:
        print(f"❌ Error en test modelo: {e}")
        return False

def test_formulario():
    """Test del formulario con años"""
    print("\n=== TEST FORMULARIO ===")
    
    try:
        form = DeclaracionVolumenForm()
        
        # Verificar campo año
        if 'ano' in form.fields:
            print("✅ Campo 'ano' encontrado")
            
            # Verificar opciones
            ano_field = form.fields['ano']
            if hasattr(ano_field.widget, 'choices'):
                choices = list(ano_field.widget.choices)
                print(f"Opciones en combobox: {len(choices)}")
                
                # Mostrar primeras opciones
                print("Primeras opciones:")
                for i, (value, label) in enumerate(choices[:6]):
                    print(f"  {i+1}. Valor: '{value}', Texto: '{label}'")
                
                return len(choices) > 1  # Al menos opción vacía + años
            else:
                print("❌ Campo año no tiene opciones")
                return False
        else:
            print("❌ Campo 'ano' no encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Error en test formulario: {e}")
        return False

def test_integracion():
    """Test de integración completo"""
    print("\n=== TEST INTEGRACIÓN ===")
    
    modelo_ok = test_modelo_anos()
    formulario_ok = test_formulario()
    
    if modelo_ok and formulario_ok:
        print("\n✅ TODOS LOS TESTS PASARON")
        print("El combobox de años debería funcionar correctamente")
        return True
    else:
        print("\n❌ ALGUNOS TESTS FALLARON")
        if not modelo_ok:
            print("- Problema con modelo/datos de años")
        if not formulario_ok:
            print("- Problema con formulario")
        return False

if __name__ == "__main__":
    print("🧪 TEST COMBOBOX DE AÑOS - DECLARACIÓN VOLUMEN")
    print("=" * 50)
    
    resultado = test_integracion()
    
    if not resultado:
        print("\n💡 Sugerencias:")
        print("1. Ejecutar: python poblar_tabla_anos.py")
        print("2. Verificar configuración de Django")
        print("3. Revisar imports en formulario")
