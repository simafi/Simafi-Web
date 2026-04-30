"""
Auditoría simple de DB para SIMAFI (Django).

Uso:
  # MySQL local (según tu caso)
  set DJANGO_DB_ENGINE=mysql
  set DJANGO_MYSQL_DB_NAME=bdsimafipy
  set DJANGO_MYSQL_DB_USER=root
  set DJANGO_MYSQL_DB_PASSWORD=sandres
  set DJANGO_MYSQL_DB_HOST=localhost
  set DJANGO_MYSQL_DB_PORT=3307
  python backend/tributario/manage.py migrate --plan
  python backend/tributario/db_audit.py --counts

  # Producción Postgres (ejecutar en el servidor con env vars de prod)
  python backend/tributario/db_audit.py --counts --pg-fast-counts
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime


def _setup_django() -> None:
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    backend_dir = os.path.join(repo_root, "backend")
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tributario_app.settings")

    import django  # noqa: WPS433

    django.setup()


def _is_postgres(vendor: str) -> bool:
    return vendor.lower() == "postgresql"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--counts", action="store_true", help="Incluir conteos por tabla")
    parser.add_argument(
        "--pg-fast-counts",
        action="store_true",
        help="En Postgres usa estimación por pg_class (rápido, no exacto).",
    )
    args = parser.parse_args()

    _setup_django()

    from django.db import connection  # noqa: WPS433

    vendor = connection.vendor
    introspection = connection.introspection

    with connection.cursor() as cursor:
        tables = sorted(introspection.table_names(cursor))

    report: dict[str, object] = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "db_vendor": vendor,
        "db_name": connection.settings_dict.get("NAME"),
        "tables": {},
    }

    with connection.cursor() as cursor:
        for table in tables:
            cols = introspection.get_table_description(cursor, table)
            constraints = introspection.get_constraints(cursor, table)
            table_info: dict[str, object] = {
                "columns": [
                    {
                        "name": c.name,
                        "type_code": getattr(c, "type_code", None),
                        "null_ok": getattr(c, "null_ok", None),
                        "internal_size": getattr(c, "internal_size", None),
                        "precision": getattr(c, "precision", None),
                        "scale": getattr(c, "scale", None),
                        "default": getattr(c, "default", None),
                    }
                    for c in cols
                ],
                "constraints": constraints,
            }

            if args.counts:
                if _is_postgres(vendor) and args.pg_fast_counts:
                    cursor.execute(
                        """
                        SELECT COALESCE(c.reltuples::bigint, 0)::bigint
                        FROM pg_class c
                        JOIN pg_namespace n ON n.oid = c.relnamespace
                        WHERE c.relname = %s
                        ORDER BY n.nspname = 'public' DESC
                        LIMIT 1
                        """,
                        [table],
                    )
                    est = cursor.fetchone()
                    table_info["rowcount_estimate"] = int(est[0] or 0) if est else 0
                else:
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {connection.ops.quote_name(table)}")
                        table_info["rowcount"] = int(cursor.fetchone()[0])
                    except Exception as exc:  # pragma: no cover
                        table_info["rowcount_error"] = str(exc)

            report["tables"][table] = table_info

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

