import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, "backend", "tributario"))
sys.path.insert(0, os.path.join(BASE_DIR, "venv", "Scripts"))

os.environ["DJANGO_SECURE_SSL_REDIRECT"] = "0"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tributario.tributario_app.settings")

import django
django.setup()

from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware

factory = RequestFactory()

def run_view(view_func, url):
    request = factory.get(url)
    
    # Add minimal required attributes for views
    middleware = SessionMiddleware(lambda req: None)
    middleware.process_request(request)
    request.session.save()
    
    msg_middleware = MessageMiddleware(lambda req: None)
    msg_middleware.process_request(request)
    
    # Bypass auth
    class DummyUser:
        is_authenticated = True
        username = "test_user"
    request.user = DummyUser()
    request.session['municipio_codigo'] = '0301'
    request.session['empresa'] = '0301'
    
    try:
        response = view_func(request)
        print(f"URL: {url} - Status: {response.status_code}")
        if response.status_code == 500:
            print(f"Content: {response.content.decode('utf-8')[:500]}")
    except Exception as e:
        print(f"CRASH on {url}: {e}")
        import traceback
        traceback.print_exc()

# Test Maestro Negocios (modern)
from tributario.views import maestro_negocios
print("Testing maestro_negocios (modern)...")
run_view(maestro_negocios, '/tributario/maestro-negocios/')

# Test Gestionar Mora Bienes (legacy)
from tributario_app.views import gestionar_mora_bienes
print("Testing gestionar_mora_bienes (legacy)...")
run_view(gestionar_mora_bienes, '/tributario-legacy/gestionar-mora-bienes/')

