"""
Migración MySQL -> PostgreSQL (estructura + datos) usando solo Python.

Pensado para Windows donde `mysqldump`, `mysql`, `psql` o `pgloader` no están en PATH.

Requisitos (ya están en requirements.txt de este repo):
  - PyMySQL
  - psycopg[binary]

Uso (PowerShell):
  $env:MYSQL_HOST='localhost'
  $env:MYSQL_PORT='3307'
  $env:MYSQL_DB='bdsimafipy'
  $env:MYSQL_USER='root'
  $env:MYSQL_PASSWORD='sandres'

  $env:PG_HOST='localhost'
  $env:PG_PORT='5432'
  $env:PG_DB='bdsimafi'
  $env:PG_USER='postgres'
  $env:PG_PASSWORD='TU_PASSWORD'   # si aplica

  python backend\\tributario\\mysql_to_postgres.py --create-db --drop-public --schema --data

Notas:
  - Crea tablas en el schema `public`.
  - Migra PKs; no migra (por ahora) FKs/índices secundarios.
  - Hace mapping de tipos comunes. Si encuentra un tipo raro, lo convierte a TEXT.
"""

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass
from typing import Any

import pymysql
import psycopg
from psycopg import sql


def env(key: str, default: str = "") -> str:
    return (os.environ.get(key) or default).strip()


@dataclass(frozen=True)
class MysqlConn:
    host: str
    port: int
    db: str
    user: str
    password: str


@dataclass(frozen=True)
class PgConn:
    host: str
    port: int
    db: str
    user: str
    password: str


def mysql_connect(cfg: MysqlConn):
    return pymysql.connect(
        host=cfg.host,
        port=cfg.port,
        user=cfg.user,
        password=cfg.password,
        database=cfg.db,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )


def pg_connect(cfg: PgConn, *, db_override: str | None = None):
    return psycopg.connect(
        host=cfg.host,
        port=cfg.port,
        dbname=db_override or cfg.db,
        user=cfg.user,
        password=cfg.password or None,
        autocommit=True,
    )


def ensure_db(cfg: PgConn) -> None:
    # Conecta a postgres default DB para crear destino si no existe
    with pg_connect(cfg, db_override="postgres") as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (cfg.db,))
            exists = cur.fetchone() is not None
            if not exists:
                cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(cfg.db)))


def drop_public_schema(cfg: PgConn) -> None:
    with pg_connect(cfg) as conn:
        with conn.cursor() as cur:
            cur.execute("DROP SCHEMA IF EXISTS public CASCADE")
            cur.execute("CREATE SCHEMA public")


def fetch_mysql_tables(mconn) -> list[str]:
    with mconn.cursor() as cur:
        cur.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = DATABASE()
              AND table_type = 'BASE TABLE'
            ORDER BY table_name
            """
        )
        rows = cur.fetchall()
        # Some MySQL setups return uppercase keys in DictCursor (e.g. TABLE_NAME)
        out = []
        for r in rows:
            if "table_name" in r:
                out.append(r["table_name"])
            elif "TABLE_NAME" in r:
                out.append(r["TABLE_NAME"])
            else:
                raise KeyError(f"Unexpected table name key(s): {list(r.keys())}")
        return out


def fetch_mysql_columns(mconn, table: str) -> list[dict[str, Any]]:
    with mconn.cursor() as cur:
        cur.execute(
            """
            SELECT
              column_name,
              data_type,
              column_type,
              is_nullable,
              column_default,
              character_maximum_length,
              numeric_precision,
              numeric_scale,
              datetime_precision,
              extra
            FROM information_schema.columns
            WHERE table_schema = DATABASE()
              AND table_name = %s
            ORDER BY ordinal_position
            """,
            (table,),
        )
        rows = list(cur.fetchall())
        if not rows:
            return rows
        # Normalize to lowercase keys for downstream mapping
        norm = []
        for r in rows:
            norm.append({str(k).lower(): v for k, v in r.items()})
        return norm


def fetch_mysql_primary_key(mconn, table: str) -> list[str]:
    with mconn.cursor() as cur:
        cur.execute(
            """
            SELECT kcu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
              ON tc.constraint_name = kcu.constraint_name
             AND tc.table_schema = kcu.table_schema
             AND tc.table_name = kcu.table_name
            WHERE tc.table_schema = DATABASE()
              AND tc.table_name = %s
              AND tc.constraint_type = 'PRIMARY KEY'
            ORDER BY kcu.ordinal_position
            """,
            (table,),
        )
        rows = cur.fetchall()
        out = []
        for r in rows:
            if "column_name" in r:
                out.append(r["column_name"])
            elif "COLUMN_NAME" in r:
                out.append(r["COLUMN_NAME"])
            else:
                raise KeyError(f"Unexpected PK key(s): {list(r.keys())}")
        return out


def map_mysql_to_pg(col: dict[str, Any]) -> sql.SQL:
    dt = (col.get("data_type") or "").lower()
    ct = (col.get("column_type") or "").lower()

    char_len = col.get("character_maximum_length")
    prec = col.get("numeric_precision")
    scale = col.get("numeric_scale")

    # boolean heuristic
    if dt == "tinyint" and ct.startswith("tinyint(1"):
        return sql.SQL("boolean")

    if dt in ("int", "integer", "mediumint"):
        return sql.SQL("integer")
    if dt == "bigint":
        return sql.SQL("bigint")
    if dt == "smallint":
        return sql.SQL("smallint")

    if dt in ("decimal", "numeric"):
        if prec is not None and scale is not None:
            return sql.SQL("numeric({},{})").format(sql.Literal(int(prec)), sql.Literal(int(scale)))
        return sql.SQL("numeric")

    if dt in ("double", "float", "real"):
        return sql.SQL("double precision")

    if dt in ("varchar", "char"):
        if char_len:
            return sql.SQL("varchar({})").format(sql.Literal(int(char_len)))
        return sql.SQL("text")

    if dt in ("text", "longtext", "mediumtext", "tinytext"):
        return sql.SQL("text")

    if dt in ("datetime", "timestamp"):
        return sql.SQL("timestamp")
    if dt == "date":
        return sql.SQL("date")
    if dt == "time":
        return sql.SQL("time")

    if dt in ("blob", "longblob", "mediumblob", "tinyblob", "binary", "varbinary"):
        return sql.SQL("bytea")

    # fallback
    return sql.SQL("text")


def _is_mysql_bool(col: dict[str, Any]) -> bool:
    dt = (col.get("data_type") or "").lower()
    ct = (col.get("column_type") or "").lower()
    return dt == "tinyint" and ct.startswith("tinyint(1")


def create_table_pg(pconn, table: str, cols: list[dict[str, Any]], pk: list[str]) -> None:
    parts: list[sql.SQL] = []
    for c in cols:
        name = c["column_name"]
        is_nullable = (c.get("is_nullable") or "YES").upper() == "YES"
        extra = (c.get("extra") or "").lower()

        col_type = map_mysql_to_pg(c)

        # identity for auto_increment integer-ish
        if "auto_increment" in extra:
            # prefer identity on integer/bigint types
            if col_type.as_string(pconn).lower() in ("integer", "bigint", "smallint"):
                col_sql = sql.SQL("{} {} GENERATED BY DEFAULT AS IDENTITY").format(
                    sql.Identifier(name),
                    col_type,
                )
            else:
                col_sql = sql.SQL("{} {}").format(sql.Identifier(name), col_type)
        else:
            col_sql = sql.SQL("{} {}").format(sql.Identifier(name), col_type)

        if not is_nullable:
            col_sql = col_sql + sql.SQL(" NOT NULL")

        parts.append(col_sql)

    if pk:
        parts.append(
            sql.SQL("PRIMARY KEY ({})").format(sql.SQL(", ").join([sql.Identifier(c) for c in pk]))
        )

    q = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({})").format(
        sql.Identifier(table),
        sql.SQL(", ").join(parts),
    )
    with pconn.cursor() as cur:
        cur.execute(q)


def copy_table_data(mconn, pconn, table: str, cols: list[dict[str, Any]], batch_size: int = 5000) -> None:
    col_names = [c["column_name"] for c in cols]
    bool_cols = {c["column_name"] for c in cols if _is_mysql_bool(c)}
    quoted_cols = sql.SQL(", ").join([sql.Identifier(c) for c in col_names])
    insert_q = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
        sql.Identifier(table),
        quoted_cols,
        sql.SQL(", ").join([sql.Placeholder()] * len(col_names)),
    )

    # stream from MySQL
    with mconn.cursor() as mcur:
        # Build a plain MySQL SELECT with backtick-quoting to avoid keyword issues.
        def qident(name: str) -> str:
            safe = name.replace("`", "``")
            return f"`{safe}`"

        select_sql = f"SELECT {', '.join(qident(c) for c in col_names)} FROM {qident(table)}"
        mcur.execute(select_sql)

        rows = mcur.fetchmany(batch_size)
        total = 0
        while rows:
            values = []
            for r in rows:
                row_out = []
                for c in col_names:
                    v = r.get(c)
                    if c in bool_cols and v is not None:
                        # MySQL tinyint(1) -> Postgres boolean
                        try:
                            v = bool(int(v))
                        except Exception:
                            v = bool(v)
                    row_out.append(v)
                values.append(tuple(row_out))
            with pconn.cursor() as pcur:
                pcur.executemany(insert_q, values)
            total += len(values)
            rows = mcur.fetchmany(batch_size)

    # NOTE: executemany is slower than COPY, but avoids CSV/encoding edge cases.
    # For typical SIMAFI sizes should still be acceptable.


def reset_table_sequences(pconn, table: str, cols: list[dict[str, Any]]) -> None:
    """
    Después de copiar datos preservando IDs, alinear secuencias para columnas identity/serial
    (evita "duplicate key" al insertar nuevos registros).
    """
    auto_cols = [c["column_name"] for c in cols if "auto_increment" in (c.get("extra") or "").lower()]
    if not auto_cols:
        return
    with pconn.cursor() as cur:
        for col in auto_cols:
            cur.execute("SELECT pg_get_serial_sequence(%s, %s)", (table, col))
            seq = cur.fetchone()[0]
            if not seq:
                continue
            cur.execute(sql.SQL("SELECT COALESCE(MAX({}), 0) FROM {}").format(
                sql.Identifier(col),
                sql.Identifier(table),
            ))
            max_id = int(cur.fetchone()[0] or 0)
            cur.execute("SELECT setval(%s, %s, true)", (seq, max_id))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--create-db", action="store_true", help="Crear PG_DB si no existe")
    ap.add_argument("--drop-public", action="store_true", help="Borrar y recrear schema public (DESTRUCTIVO)")
    ap.add_argument("--schema", action="store_true", help="Crear tablas")
    ap.add_argument("--data", action="store_true", help="Copiar datos")
    ap.add_argument("--only", action="append", default=[], help="Migrar solo esta tabla (repetible)")
    ap.add_argument("--skip", action="append", default=[], help="Saltar esta tabla (repetible)")
    args = ap.parse_args()

    mysql_cfg = MysqlConn(
        host=env("MYSQL_HOST", "localhost"),
        port=int(env("MYSQL_PORT", "3307") or "3307"),
        db=env("MYSQL_DB", "bdsimafipy"),
        user=env("MYSQL_USER", "root"),
        password=env("MYSQL_PASSWORD", ""),
    )
    pg_cfg = PgConn(
        host=env("PG_HOST", "localhost"),
        port=int(env("PG_PORT", "5432") or "5432"),
        db=env("PG_DB", "bdsimafi"),
        user=env("PG_USER", "postgres"),
        password=env("PG_PASSWORD", ""),
    )

    if args.create_db:
        ensure_db(pg_cfg)

    if args.drop_public:
        drop_public_schema(pg_cfg)

    only = set(args.only or [])
    skip = set(args.skip or [])

    with mysql_connect(mysql_cfg) as mconn, pg_connect(pg_cfg) as pconn:
        tables = fetch_mysql_tables(mconn)
        if only:
            tables = [t for t in tables if t in only]
        if skip:
            tables = [t for t in tables if t not in skip]

        for t in tables:
            cols = fetch_mysql_columns(mconn, t)
            pk = fetch_mysql_primary_key(mconn, t)

            if args.schema:
                create_table_pg(pconn, t, cols, pk)
            if args.data:
                # truncate first to be idempotent-ish
                with pconn.cursor() as cur:
                    cur.execute(sql.SQL("TRUNCATE TABLE {} RESTART IDENTITY").format(sql.Identifier(t)))
                copy_table_data(mconn, pconn, t, cols)
                reset_table_sequences(pconn, t, cols)

            print(f"OK {t}", flush=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

