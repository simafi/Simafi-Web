import os
import sys
import logging
import traceback
from pathlib import Path


# Repo root: .../api/index.py -> repo/
REPO_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = REPO_ROOT / "backend"

# Django necesita encontrar:
# - `urls.py` (ROOT_URLCONF='urls') dentro de backend/
# - paquete `tributario` dentro de backend/
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

# Importar tributario_app requiere que su padre esté en el path
# BACKEND_DIR ya contiene a tributario/ y tributario/ contiene tributario_app/
# Por seguridad, nos aseguramos que el directorio de la app específica esté disponible
TRIBUTARIO_DIR = BACKEND_DIR / "tributario"
if str(TRIBUTARIO_DIR) not in sys.path:
    sys.path.insert(0, str(TRIBUTARIO_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tributario.tributario_app.settings")

logger = logging.getLogger("vercel.entrypoint")

if not logging.getLogger().handlers:
    logging.basicConfig(
        level=os.environ.get("LOG_LEVEL", "INFO").upper(),
        format="%(levelname)s %(name)s: %(message)s",
    )


def _log_startup_context() -> None:
    """
    Logs non-secret hints to help diagnose Vercel cold-start crashes.
    Never log full connection strings.
    """
    keys = [
        "VERCEL",
        "DJANGO_VERCEL",
        "DJANGO_DEBUG",
        "DJANGO_SETTINGS_MODULE",
        "DJANGO_DATABASE_URL",
        "DATABASE_URL",
        "POSTGRES_URL",
        "PRISMA_DATABASE_URL",
        "DJANGO_DB_HOST",
        "DJANGO_DB_NAME",
        "DJANGO_DB_USER",
    ]
    present = {k: ("set" if (os.environ.get(k) or "").strip() else "missing") for k in keys}
    sk = (os.environ.get("DJANGO_SECRET_KEY") or "").strip()
    present["DJANGO_SECRET_KEY"] = f"len={len(sk)}" if sk else "missing"
    logger.warning("Vercel Django startup context: %s", present)


_log_startup_context()

from django.core.wsgi import get_wsgi_application  # noqa: E402

# Vercel's static analyzer expects a top-level binding like `app = ...`
# Keep imports outside try/except; only wrap initialization for stderr diagnostics.
try:
    app = get_wsgi_application()
    application = app
except Exception:
    print("--- VERCEL STARTUP ERROR ---", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    print("----------------------------", file=sys.stderr)
    raise

