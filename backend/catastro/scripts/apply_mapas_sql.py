# -*- coding: utf-8 -*-
"""
Aplica backend/catastro/sql/mapas_simafi_supabase.sql vía psycopg (sin psql).

Uso un solo paso (carpeta backend/):
  1) En la raíz del repo, archivo .env.supabase_prod o .env con DATABASE_URL=postgresql://...
  2)  python catastro/scripts/apply_mapas_sql.py

O defina la URL en el entorno (PowerShell: $env:DATABASE_URL = "postgresql://...").

Variables (la primera con valor gana): DIRECT_URL, DATABASE_URL, DJANGO_DATABASE_URL,
SUPABASE_DATABASE_URL. En Supabase, si el pooler falla al crear tablas, use URI directa (puerto 5432).
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

_SQL_FILE = Path(__file__).resolve().parent.parent / "sql" / "mapas_simafi_supabase.sql"
# apply_mapas_sql.py -> scripts -> catastro -> backend
_BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
_REPO_ROOT = _BACKEND_DIR.parent
_URL_KEYS = (
    "DIRECT_URL",
    "DATABASE_URL",
    "DJANGO_DATABASE_URL",
    "SUPABASE_DATABASE_URL",
)


def _try_load_dotenv() -> None:
    """Carga DATABASE_URL desde archivos .env en la raíz del repo (sin pisar variables ya definidas)."""
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    for name in (
        ".env",
        ".env.local",
        ".env.supabase_dev",
        ".env.supabase_prod",
    ):
        path = _REPO_ROOT / name
        if path.is_file():
            load_dotenv(path, override=False)


def _database_url() -> str:
    for key in _URL_KEYS:
        v = (os.environ.get(key) or "").strip()
        if v:
            return v
    print(
        "Error: defina al menos una variable de entorno con la URL de Postgres,",
        "por ejemplo DATABASE_URL o DIRECT_URL (Supabase).",
        file=sys.stderr,
    )
    sys.exit(1)


def _load_statements(sql_path: Path) -> list[str]:
    text = sql_path.read_text(encoding="utf-8")
    # Quitar líneas que son solo comentario -- (no toca bloques /* */ en este .sql)
    lines = [ln for ln in text.splitlines() if not ln.lstrip().startswith("--")]
    body = "\n".join(lines)
    # Partir en sentencias por ';' (este archivo no tiene ; dentro de strings)
    out: list[str] = []
    for chunk in body.split(";"):
        s = chunk.strip()
        if not s:
            continue
        up = s.upper()
        if up == "BEGIN" or up == "COMMIT":
            continue
        out.append(s)
    return out


def main() -> None:
    _try_load_dotenv()

    if not _SQL_FILE.is_file():
        print(f"No existe {_SQL_FILE}", file=sys.stderr)
        sys.exit(1)

    try:
        import psycopg
    except ImportError:
        print(
            "Instale psycopg: pip install \"psycopg[binary]>=3.2\"",
            file=sys.stderr,
        )
        sys.exit(1)

    dsn = _database_url()
    stmts = _load_statements(_SQL_FILE)
    if not stmts:
        print("No hay sentencias SQL que ejecutar.", file=sys.stderr)
        sys.exit(1)

    # Resumir conexión sin mostrar contraseña
    host = re.sub(r":[^@/]+@", ":****@", dsn) if "@" in dsn else dsn
    print(f"Conectando: {host[:80]}{'...' if len(host) > 80 else ''}")
    print(f"Sentencias: {len(stmts)} (BEGIN/COMMIT del .sql se omiten; una sola transacción)")

    with psycopg.connect(dsn) as conn:
        with conn.transaction():
            with conn.cursor() as cur:
                for i, stmt in enumerate(stmts, 1):
                    cur.execute(stmt)
                    head = (stmt.split()[0] if stmt else "")[:24]
                    print(f"  OK {i}/{len(stmts)} {head!r}...")

    print("Listo: tablas Mapas Simafi aplicadas en la base de datos.")


if __name__ == "__main__":
    main()
