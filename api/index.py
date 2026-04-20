import os
import sys
from pathlib import Path


# Repo root: .../api/index.py -> repo/
REPO_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = REPO_ROOT / "backend"
TRIBUTARIO_DIR = BACKEND_DIR / "tributario"

# Django necesita encontrar:
# - `urls.py` (ROOT_URLCONF='urls') dentro de backend/
# - paquete `tributario` dentro de backend/
sys.path.insert(0, str(BACKEND_DIR))
sys.path.insert(0, str(TRIBUTARIO_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tributario.tributario_app.settings")

from django.core.wsgi import get_wsgi_application  # noqa: E402

app = get_wsgi_application()

