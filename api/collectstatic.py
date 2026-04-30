import os
import sys
from pathlib import Path


# Repo root: .../api/collectstatic.py -> repo/
REPO_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = REPO_ROOT / "backend"
TRIBUTARIO_DIR = BACKEND_DIR / "tributario"

sys.path.insert(0, str(BACKEND_DIR))
sys.path.insert(0, str(TRIBUTARIO_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tributario_app.settings")


def main() -> None:
    import django
    django.setup()
    from django.core.management import call_command

    run_migrations = (
        (os.environ.get("VERCEL") or "").strip().lower() in ("1", "true", "yes", "on")
        or (os.environ.get("DJANGO_VERCEL") or "").strip().lower() in ("1", "true", "yes", "on")
        or (os.environ.get("VERCEL_ENV") or "").strip().lower() == "production"
        or (os.environ.get("DJANGO_RUN_MIGRATIONS") or "").strip().lower() in ("1", "true", "yes", "on")
    )
    if run_migrations:
        # En Supabase, es común usar PgBouncer/pooler para runtime (DATABASE_URL con ?pgbouncer=true),
        # pero para migraciones conviene una conexión directa (sin pooler) para evitar errores.
        direct_url = (os.environ.get("DIRECT_URL") or "").strip()
        if direct_url:
            os.environ["DATABASE_URL"] = direct_url
            print("Vercel build: running migrate --noinput (using DIRECT_URL)")
        else:
            print("Vercel build: running migrate --noinput")
        call_command("migrate", "--noinput")
    else:
        print("Vercel build: skipping migrate (set DJANGO_RUN_MIGRATIONS=1 to force)")

    call_command("collectstatic", "--noinput")


if __name__ == "__main__":
    main()

