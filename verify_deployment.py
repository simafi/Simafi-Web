import os
import sys
import django
from pathlib import Path

def verify():
    print("--- SIMAFI Deployment Readiness Check ---")
    
    # 1. Paths
    repo_root = Path(__file__).resolve().parent
    backend_dir = repo_root / "backend"
    tributario_dir = backend_dir / "tributario"
    
    sys.path.insert(0, str(backend_dir))
    sys.path.insert(0, str(tributario_dir))
    
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tributario_app.settings")
    
    try:
        django.setup()
        print("[OK] Django setup successful.")
    except Exception as e:
        print(f"[FAIL] Django setup failed: {e}")
        return

    # 2. Model Conflicts
    from django.apps import apps
    try:
        apps.get_models()
        print("[OK] No model registration conflicts detected.")
    except Exception as e:
        print(f"[FAIL] Model conflict detected: {e}")

    # 3. Template Resolution
    from django.template.loader import get_template
    templates_to_check = [
        'contabilidad_ejercicio_form.html',
        'contabilidad_base.html',
    ]
    for t in templates_to_check:
        try:
            get_template(t)
            print(f"[OK] Template found: {t}")
        except Exception:
            print(f"[FAIL] Template NOT found: {t}")

    # 4. URL Resolution
    from django.urls import reverse
    try:
        url = reverse('contabilidad:ejercicio_crear')
        print(f"[OK] URL resolved: {url}")
    except Exception as e:
        print(f"[FAIL] URL resolution failed: {e}")

    print("\n--- Summary ---")
    print("If all checks are [OK], your local code is ready for deployment.")
    print("Make sure to PUSH these changes to your repository and redeploy on Vercel.")

if __name__ == "__main__":
    verify()
