#!/usr/bin/env python
"""
Test script to verify the declaracion_volumen VariableDoesNotExist fix
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

def test_declaracion_volumen_with_negocio():
    """Test declaracion_volumen view with RTM and EXPE parameters"""
    try:
        # Create a mock request with RTM and EXPE parameters
        factory = RequestFactory()
        request = factory.get('/tributario/declaracion-volumen/?rtm=12345&expe=67890')
        
        # Call the view
        response = declaracion_volumen(request)
        
        # Check if the response is successful
        if response.status_code == 200:
            print("✅ SUCCESS: declaracion_volumen view rendered successfully with negocio data")
            
            # Check if the context contains the negocio variable
            context = response.context_data
            if 'negocio' in context and context['negocio'] is not None:
                negocio = context['negocio']
                print(f"   - RTM: {negocio.rtm}")
                print(f"   - EXPE: {negocio.expe}")
                print(f"   - Nombre: {negocio.nombrenego}")
                print(f"   - Comerciante: {negocio.comerciante}")
                return True
            else:
                print("❌ ERROR: negocio variable not found in context")
                return False
        else:
            print(f"❌ ERROR: View returned status code {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: declaracion_volumen view failed: {e}")
        return False

def test_declaracion_volumen_without_negocio():
    """Test declaracion_volumen view without RTM and EXPE parameters"""
    try:
        # Create a mock request without parameters
        factory = RequestFactory()
        request = factory.get('/tributario/declaracion-volumen/')
        
        # Call the view
        response = declaracion_volumen(request)
        
        # Check if the response is successful
        if response.status_code == 200:
            print("✅ SUCCESS: declaracion_volumen view rendered successfully without negocio data")
            
            # Check if the context contains the negocio variable (should be None)
            context = response.context_data
            if 'negocio' in context:
                print(f"   - negocio variable present: {context['negocio'] is not None}")
                return True
            else:
                print("❌ ERROR: negocio variable not found in context")
                return False
        else:
            print(f"❌ ERROR: View returned status code {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: declaracion_volumen view failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing declaracion_volumen VariableDoesNotExist fix...")
    print("=" * 60)
    
    # Test 1: With negocio data
    print("\n1. Testing with RTM and EXPE parameters:")
    test1 = test_declaracion_volumen_with_negocio()
    
    # Test 2: Without negocio data
    print("\n2. Testing without RTM and EXPE parameters:")
    test2 = test_declaracion_volumen_without_negocio()
    
    # Summary
    print("\n" + "=" * 60)
    if test1 and test2:
        print("🎉 ALL TESTS PASSED! VariableDoesNotExist error should be fixed.")
        print("   The template should now render without the negocio variable error.")
    else:
        print("⚠️  Some tests failed. The error may still exist.")
















