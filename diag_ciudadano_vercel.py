"""
Diagnóstico del error 500 - simulando EXACTAMENTE el entorno de Vercel (api/index.py)
"""
import os, sys, traceback
from pathlib import Path

# Simular api/index.py de Vercel
REPO_ROOT = Path(r'C:\simafiweb')
BACKEND_DIR = REPO_ROOT / "backend"
TRIBUTARIO_DIR = BACKEND_DIR / "tributario"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(TRIBUTARIO_DIR) not in sys.path:
    sys.path.insert(0, str(TRIBUTARIO_DIR))

os.environ['DJANGO_SETTINGS_MODULE'] = 'tributario.tributario_app.settings'
os.environ['DATABASE_URL'] = (
    'postgresql://postgres.inzasugoozqqnelcvrwd:Sandres0318$$'
    '@aws-1-us-west-2.pooler.supabase.com:5432/postgres'
)
os.environ['DJANGO_VERCEL'] = '1'
os.environ['DJANGO_SECRET_KEY'] = '7$n&2!k@p*9zL#5vQ(r6wX+3mB)Y4eA1dG8hJ0uS2cNfG7xT3iP'
os.environ['DJANGO_DEBUG'] = '0'

print(f"sys.path[0:3] = {sys.path[:3]}")
print(f"DJANGO_SETTINGS_MODULE = {os.environ['DJANGO_SETTINGS_MODULE']}")

import django
try:
    django.setup()
    print("Django setup OK\n")
except Exception as e:
    print(f"ERROR en django.setup(): {e}")
    traceback.print_exc()
    sys.exit(1)

tests = [
    ("Importar vista nueva_solicitud",
     "from ciudadano.views import nueva_solicitud; print('  OK')"),
    ("Instanciar SolicitudTramiteForm",
     "from ciudadano.forms import SolicitudTramiteForm; f=SolicitudTramiteForm(); print(f'  OK - campos: {list(f.fields.keys())}')"),
    ("Consultar SolicitudTramite en DB",
     "from ciudadano.models import SolicitudTramite; c=SolicitudTramite.objects.count(); print(f'  OK - count={c}')"),
    ("Resolver URL ciudadano:nueva_solicitud",
     "from django.urls import reverse; u=reverse('ciudadano:nueva_solicitud'); print(f'  OK - {u}')"),
    ("Resolver URL ciudadano:menu_ciudadano",
     "from django.urls import reverse; u=reverse('ciudadano:menu_ciudadano'); print(f'  OK - {u}')"),
    ("Resolver URL ciudadano:mis_solicitudes",
     "from django.urls import reverse; u=reverse('ciudadano:mis_solicitudes'); print(f'  OK - {u}')"),
    ("Cargar template solicitud_form.html",
     "from django.template.loader import get_template; t=get_template('ciudadano/solicitud_form.html'); print(f'  OK - {t.origin}')"),
    ("Cargar template base_ciudadano.html",
     "from django.template.loader import get_template; t=get_template('ciudadano/base_ciudadano.html'); print(f'  OK - {t.origin}')"),
    ("Importar notificaciones ciudadano",
     "from ciudadano.notificaciones import construir_mensaje_whatsapp; print('  OK')"),
    ("Resolver URL modules_core:login_principal",
     "from django.urls import reverse; u=reverse('modules_core:login_principal'); print(f'  OK - {u}')"),
    ("Resolver URL modules_core:menu_principal",
     "from django.urls import reverse; u=reverse('modules_core:menu_principal'); print(f'  OK - {u}')"),
]

all_ok = True
for name, code in tests:
    print(f"TEST: {name}")
    try:
        exec(code)
    except Exception as e:
        print(f"  FALLO: {e}")
        traceback.print_exc()
        all_ok = False

print("\n" + ("="*50))
if all_ok:
    print("TODOS LOS TESTS PASARON - El problema es otro (sesion/CSRF/middleware?)")
else:
    print("SE ENCONTRARON ERRORES - Ver detalle arriba")
