#!/usr/bin/env python
"""
Test script to verify the declaracion_volumen form is working correctly
"""
import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
sys.path.insert(0, r'C:\simafiweb\venv\Scripts\tributario')

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from django.test import RequestFactory
from modules.tributario.simple_views import declaracion_volumen
from tributario_app.forms import DeclaracionVolumenForm

def test_formulario_declaracion():
    """Test that the declaracion_volumen form is properly rendered"""
    try:
        # Create a mock request with RTM and EXPE parameters
        factory = RequestFactory()
        request = factory.get('/tributario/declaracion-volumen/?rtm=12345&expe=67890')
        
        # Call the view
        response = declaracion_volumen(request)
        
        # Check if the response is successful
        if response.status_code == 200:
            print("✅ SUCCESS: declaracion_volumen view rendered successfully")
            
            # Check if the context contains the form
            context = response.context_data
            if 'form' in context:
                form = context['form']
                print(f"   - Form type: {type(form).__name__}")
                print(f"   - Form fields: {list(form.fields.keys())}")
                
                # Check specific fields that should be present
                expected_fields = ['ventai', 'ventac', 'ventas', 'valorexcento', 'controlado', 'impuesto']
                missing_fields = []
                for field in expected_fields:
                    if field not in form.fields:
                        missing_fields.append(field)
                
                if missing_fields:
                    print(f"❌ ERROR: Missing form fields: {missing_fields}")
                    return False
                else:
                    print("✅ SUCCESS: All expected form fields are present")
                    return True
            else:
                print("❌ ERROR: form not found in context")
                return False
        else:
            print(f"❌ ERROR: View returned status code {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: declaracion_volumen view failed: {e}")
        return False

def test_formulario_creation():
    """Test that DeclaracionVolumenForm can be created"""
    try:
        form = DeclaracionVolumenForm()
        print("✅ SUCCESS: DeclaracionVolumenForm created successfully")
        print(f"   - Form fields: {list(form.fields.keys())}")
        return True
    except Exception as e:
        print(f"❌ ERROR: Failed to create DeclaracionVolumenForm: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing declaracion_volumen form functionality...")
    print("=" * 60)
    
    # Test 1: Form creation
    print("\n1. Testing form creation:")
    test1 = test_formulario_creation()
    
    # Test 2: View rendering with form
    print("\n2. Testing view rendering with form:")
    test2 = test_formulario_declaracion()
    
    # Summary
    print("\n" + "=" * 60)
    if test1 and test2:
        print("🎉 ALL TESTS PASSED! Form should be working correctly.")
        print("   - The form fields should now appear in the template")
        print("   - The validation and calculations should work")
    else:
        print("⚠️  Some tests failed. There may still be issues.")
















