"""
Resetear secuencias/identities en PostgreSQL para evitar errores tipo:
  duplicate key violates unique constraint "..._pkey" (id)=(N)

Útil después de migrar datos desde MySQL preservando IDs.

Uso (PowerShell):
  $env:DJANGO_DATABASE_URL='postgresql://postgres:sandres@127.0.0.1:5432/bdsimafi'
  python backend\\tributario\\reset_pg_sequences.py
"""

from __future__ import annotations

import os

import psycopg


def _env(key: str) -> str:
    return (os.environ.get(key) or "").strip()


def main() -> int:
    url = _env("DJANGO_DATABASE_URL") or _env("DATABASE_URL") or _env("DIRECT_URL")
    if not url:
        raise SystemExit("Define DJANGO_DATABASE_URL para conectar a Postgres.")

    with psycopg.connect(url, autocommit=True) as conn:
        with conn.cursor() as cur:
            # Columnas que usan secuencia:
            # - SERIAL: column_default = nextval(...)
            # - IDENTITY: is_identity = 'YES' (a veces column_default viene NULL)
            cur.execute(
                """
                SELECT table_name, column_name
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND (
                    column_default LIKE 'nextval(%'
                    OR is_identity = 'YES'
                  )
                ORDER BY table_name, column_name
                """
            )
            pairs = cur.fetchall()

            for table, col in pairs:
                # Obtiene el nombre real de la secuencia asociada
                cur.execute("SELECT pg_get_serial_sequence(%s, %s)", (table, col))
                seq = cur.fetchone()[0]
                if not seq:
                    continue
                # setval(seq, max(id), true) → nextval será max+1
                cur.execute(f'SELECT COALESCE(MAX("{col}"), 0) FROM "{table}"')
                max_id = int(cur.fetchone()[0] or 0)
                # setval no permite 0 si la secuencia inicia en 1
                target = max(1, max_id)
                cur.execute("SELECT setval(%s, %s, true)", (seq, target))
                print(f"OK reset {seq} = {target} (max={max_id})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

