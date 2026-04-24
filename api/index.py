import os
import sys
import logging
import traceback
from pathlib import Path

# Repo root: .../api/index.py -> repo/
REPO_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = REPO_ROOT / "backend"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

TRIBUTARIO_DIR = BACKEND_DIR / "tributario"
if str(TRIBUTARIO_DIR) not in sys.path:
    sys.path.insert(0, str(TRIBUTARIO_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tributario_app.settings")

logger = logging.getLogger("vercel.entrypoint")

if not logging.getLogger().handlers:
    logging.basicConfig(
        level=os.environ.get("LOG_LEVEL", "INFO").upper(),
        format="%(levelname)s %(name)s: %(message)s",
    )

def _log_startup_context() -> None:
    keys = [
        "VERCEL", "DJANGO_VERCEL", "DJANGO_DEBUG", "DJANGO_SETTINGS_MODULE",
        "DATABASE_URL", "POSTGRES_URL", "DJANGO_DB_HOST"
    ]
    present = {k: ("set" if (os.environ.get(k) or "").strip() else "missing") for k in keys}
    sk = (os.environ.get("DJANGO_SECRET_KEY") or "").strip()
    present["DJANGO_SECRET_KEY"] = f"len={len(sk)}" if sk else "missing"
    logger.warning("Vercel Django startup context: %s", present)

_log_startup_context()

def _create_error_handler(error_msg: str):
    def error_handler(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        return [error_msg.encode('utf-8')]
    return error_handler

try:
    from django.core.wsgi import get_wsgi_application
    app = get_wsgi_application()
except Exception:
    error_traceback = traceback.format_exc()
    print(f"CRITICAL: Django initialization failed:\n{error_traceback}", file=sys.stderr)
    app = _create_error_handler(f"SIMAFI Startup Error\n\n{error_traceback}")

application = app
