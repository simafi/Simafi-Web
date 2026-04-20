#!/usr/bin/env python
"""
Test script to verify the NoReverseMatch fix
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

from django.urls import reverse
from django.test import RequestFactory
from modules.core.views import menu_principal

def test_tributario_login_url():
    """Test if the tributario_login URL can be resolved"""
    try:
        # Test URL resolution
        url = reverse('tributario:tributario_login')
        print(f"✅ SUCCESS: tributario_login URL resolved to: {url}")
        return True
    except Exception as e:
        print(f"❌ ERROR: Could not resolve tributario_login URL: {e}")
        return False

def test_menu_principal_view():
    """Test if the menu_principal view can be rendered without NoReverseMatch error"""
    try:
        # Create a mock request
        factory = RequestFactory()
        request = factory.get('/menu/')
        
        # Add session data
        request.session = {
            'user_id': 1,
            'nombre': 'Test User',
            'empresa': 'Test Company'
        }
        
        # Try to render the view
        response = menu_principal(request)
        print(f"✅ SUCCESS: menu_principal view rendered successfully")
        return True
    except Exception as e:
        print(f"❌ ERROR: menu_principal view failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing NoReverseMatch fix...")
    print("=" * 50)
    
    # Test 1: URL resolution
    print("\n1. Testing URL resolution:")
    url_test = test_tributario_login_url()
    
    # Test 2: View rendering
    print("\n2. Testing view rendering:")
    view_test = test_menu_principal_view()
    
    # Summary
    print("\n" + "=" * 50)
    if url_test and view_test:
        print("🎉 ALL TESTS PASSED! NoReverseMatch error should be fixed.")
    else:
        print("⚠️  Some tests failed. The error may still exist.")
















