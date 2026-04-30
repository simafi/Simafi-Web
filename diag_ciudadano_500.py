"""
Diagnóstico del error 500 en /ciudadano/solicitud/nueva/
Simula lo que hace Django al procesar esa vista para identificar el traceback real.
"""
import os, sys, django

# Configurar entorno Django local con DB de Supabase
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.tributario_app.settings')
os.environ['DATABASE_URL'] = (
    'postgresql://postgres.inzasugoozqqnelcvrwd:Sandres0318$$'
    '@aws-1-us-west-2.pooler.supabase.com:5432/postgres'
)
os.environ['DJANGO_VERCEL'] = '1'
os.environ['DJANGO_SECRET_KEY'] = '7$n&2!k@p*9zL#5vQ(r6wX+3mB)Y4eA1dG8hJ0uS2cNfG7xT3iP'

sys.path.insert(0, r'C:\simafiweb\backend')

try:
    django.setup()
    print("Django configurado OK")
except Exception as e:
    print(f"ERROR configurando Django: {e}")
    sys.exit(1)

# --- Prueba 1: importar la vista directamente ---
print("\n1. Importando vista nueva_solicitud...")
try:
    from ciudadano.views import nueva_solicitud
    print("   OK")
except Exception as e:
    print(f"   ERROR: {e}")
    import traceback; traceback.print_exc()

# --- Prueba 2: instanciar el formulario ---
print("\n2. Instanciando SolicitudTramiteForm...")
try:
    from ciudadano.forms import SolicitudTramiteForm
    form = SolicitudTramiteForm()
    print(f"   OK - campos: {list(form.fields.keys())}")
except Exception as e:
    print(f"   ERROR: {e}")
    import traceback; traceback.print_exc()

# --- Prueba 3: acceso al modelo ---
print("\n3. Consultando SolicitudTramite en DB...")
try:
    from ciudadano.models import SolicitudTramite
    count = SolicitudTramite.objects.count()
    print(f"   OK - registros: {count}")
except Exception as e:
    print(f"   ERROR: {e}")
    import traceback; traceback.print_exc()

# --- Prueba 4: resolver URL ---
print("\n4. Resolviendo URL ciudadano:nueva_solicitud...")
try:
    from django.urls import reverse
    url = reverse('ciudadano:nueva_solicitud')
    print(f"   OK - url: {url}")
except Exception as e:
    print(f"   ERROR: {e}")
    import traceback; traceback.print_exc()

# --- Prueba 5: verificar que el template existe ---
print("\n5. Cargando template ciudadano/solicitud_form.html...")
try:
    from django.template.loader import get_template
    t = get_template('ciudadano/solicitud_form.html')
    print(f"   OK - template: {t.origin}")
except Exception as e:
    print(f"   ERROR: {e}")
    import traceback; traceback.print_exc()

# --- Prueba 6: notificaciones import ---
print("\n6. Importando notificaciones ciudadano...")
try:
    from ciudadano.notificaciones import construir_mensaje_whatsapp, construir_url_whatsapp, enviar_correo_con_adjunto
    print("   OK")
except Exception as e:
    print(f"   ERROR: {e}")
    import traceback; traceback.print_exc()

print("\n--- Diagnostico completo ---")
