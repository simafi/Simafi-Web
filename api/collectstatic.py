import os
import sys
from pathlib import Path


# Repo root: .../api/collectstatic.py -> repo/
REPO_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = REPO_ROOT / "backend"
TRIBUTARIO_DIR = BACKEND_DIR / "tributario"

sys.path.insert(0, str(BACKEND_DIR))
sys.path.insert(0, str(TRIBUTARIO_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tributario.tributario_app.settings")


def main() -> None:
    import django
    django.setup()
    from django.core.management import call_command

    run_migrations = (
        (os.environ.get("VERCEL_ENV") or "").strip().lower() == "production"
        or (os.environ.get("DJANGO_RUN_MIGRATIONS") or "").strip().lower() in ("1", "true", "yes", "on")
    )
    if run_migrations:
        call_command("migrate", "--noinput")

    call_command("collectstatic", "--noinput")


if __name__ == "__main__":
    main()

