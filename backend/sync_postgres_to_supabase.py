import argparse
import io
import os
from getpass import getpass
from typing import List, Tuple

import psycopg2
from psycopg2 import sql


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sincroniza datos desde PostgreSQL local hacia Supabase (solo datos)."
    )
    parser.add_argument("--source-url", help="URL de origen PostgreSQL local.")
    parser.add_argument("--target-url", help="URL de destino Supabase.")
    parser.add_argument("--source-host", default="127.0.0.1", help="Host origen.")
    parser.add_argument("--source-port", type=int, default=5432, help="Puerto origen.")
    parser.add_argument("--source-db", default="bdsimafi", help="Base origen.")
    parser.add_argument("--source-user", default="postgres", help="Usuario origen.")
    parser.add_argument("--source-password", default="", help="Password origen.")
    parser.add_argument("--target-host", default="", help="Host destino (Supabase).")
    parser.add_argument("--target-port", type=int, default=5432, help="Puerto destino.")
    parser.add_argument("--target-db", default="postgres", help="Base destino.")
    parser.add_argument("--target-user", default="postgres", help="Usuario destino.")
    parser.add_argument("--target-password", default="", help="Password destino.")
    parser.add_argument(
        "--schema",
        default="public",
        help="Schema a copiar (por defecto: public).",
    )
    parser.add_argument(
        "--exclude",
        default="",
        help="Lista de tablas separadas por coma para excluir.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Muestra tablas a copiar sin escribir en destino.",
    )
    return parser.parse_args()


def get_tables(conn, schema: str, excluded: List[str]) -> List[str]:
    query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = %s
          AND table_type = 'BASE TABLE'
        ORDER BY table_name
    """
    with conn.cursor() as cur:
        cur.execute(query, (schema,))
        names = [r[0] for r in cur.fetchall()]
    excluded_set = {t.strip() for t in excluded if t.strip()}
    return [t for t in names if t not in excluded_set]


def intersect_tables(source_tables: List[str], target_tables: List[str]) -> Tuple[List[str], List[str]]:
    target_set = set(target_tables)
    common = [t for t in source_tables if t in target_set]
    missing_in_target = [t for t in source_tables if t not in target_set]
    return common, missing_in_target


def get_source_columns(conn, schema: str, table: str):
    query = """
        SELECT
            a.attname AS column_name,
            pg_catalog.format_type(a.atttypid, a.atttypmod) AS data_type,
            a.attnotnull AS not_null,
            pg_get_expr(ad.adbin, ad.adrelid) AS default_expr
        FROM pg_attribute a
        JOIN pg_class c ON c.oid = a.attrelid
        JOIN pg_namespace n ON n.oid = c.relnamespace
        LEFT JOIN pg_attrdef ad ON ad.adrelid = a.attrelid AND ad.adnum = a.attnum
        WHERE n.nspname = %s
          AND c.relname = %s
          AND a.attnum > 0
          AND NOT a.attisdropped
        ORDER BY a.attnum
    """
    with conn.cursor() as cur:
        cur.execute(query, (schema, table))
        return cur.fetchall()


def get_source_constraints(conn, schema: str, table: str):
    query = """
        SELECT conname, pg_get_constraintdef(oid) AS definition
        FROM pg_constraint
        WHERE conrelid = %s::regclass
          AND contype IN ('p', 'u', 'f', 'c')
        ORDER BY contype, conname
    """
    with conn.cursor() as cur:
        cur.execute(query, (f"{schema}.{table}",))
        return cur.fetchall()


def _column_definition(column_name: str, data_type: str, not_null: bool, default_expr: str) -> str:
    default_expr = (default_expr or "").strip()
    serial_map = {
        "smallint": "smallserial",
        "integer": "serial",
        "bigint": "bigserial",
    }
    if default_expr.startswith("nextval(") and data_type in serial_map:
        base = f"{column_name} {serial_map[data_type]}"
    else:
        base = f"{column_name} {data_type}"
        if default_expr:
            base += f" DEFAULT {default_expr}"
    if not_null:
        base += " NOT NULL"
    return base


def create_missing_table(source_conn, target_conn, schema: str, table: str) -> None:
    cols = get_source_columns(source_conn, schema, table)
    if not cols:
        raise RuntimeError(f"No se pudieron leer columnas de {schema}.{table}")

    col_defs = [
        _column_definition(col_name, data_type, not_null, default_expr)
        for col_name, data_type, not_null, default_expr in cols
    ]
    create_sql = (
        f'CREATE TABLE "{schema}"."{table}" (\n  ' + ",\n  ".join(col_defs) + "\n)"
    )
    with target_conn.cursor() as cur:
        cur.execute(create_sql)

    constraints = get_source_constraints(source_conn, schema, table)
    with target_conn.cursor() as cur:
        for conname, definition in constraints:
            cur.execute(
                sql.SQL('ALTER TABLE {}.{} ADD CONSTRAINT {} {}').format(
                    sql.Identifier(schema),
                    sql.Identifier(table),
                    sql.Identifier(conname),
                    sql.SQL(definition),
                )
            )


def get_columns(conn, schema: str, table: str) -> List[str]:
    query = """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = %s AND table_name = %s
        ORDER BY ordinal_position
    """
    with conn.cursor() as cur:
        cur.execute(query, (schema, table))
        return [r[0] for r in cur.fetchall()]


def get_row_count(conn, schema: str, table: str) -> int:
    with conn.cursor() as cur:
        cur.execute(
            sql.SQL("SELECT COUNT(*) FROM {}.{}").format(
                sql.Identifier(schema), sql.Identifier(table)
            )
        )
        return cur.fetchone()[0]


def copy_table_data(
    source_conn, target_conn, schema: str, table: str, columns: List[str]
) -> Tuple[int, int]:
    select_count = get_row_count(source_conn, schema, table)
    if not columns:
        return select_count, 0

    buffer = io.StringIO()
    col_identifiers = [sql.Identifier(c) for c in columns]

    copy_out = sql.SQL("COPY {}.{} ({}) TO STDOUT WITH CSV").format(
        sql.Identifier(schema),
        sql.Identifier(table),
        sql.SQL(", ").join(col_identifiers),
    )
    copy_in = sql.SQL("COPY {}.{} ({}) FROM STDIN WITH CSV").format(
        sql.Identifier(schema),
        sql.Identifier(table),
        sql.SQL(", ").join(col_identifiers),
    )

    with source_conn.cursor() as src_cur:
        src_cur.copy_expert(copy_out.as_string(source_conn), buffer)

    buffer.seek(0)
    with target_conn.cursor() as dst_cur:
        dst_cur.copy_expert(copy_in.as_string(target_conn), buffer)

    return select_count, select_count


def _resolve_password(explicit: str, env_key: str, prompt: str) -> str:
    if explicit:
        return explicit
    env_value = os.environ.get(env_key, "").strip()
    if env_value:
        return env_value
    return getpass(prompt)


def connect_from_args(args: argparse.Namespace, prefix: str):
    url_value = getattr(args, f"{prefix}_url", "") or ""
    if url_value:
        return psycopg2.connect(url_value)

    host = getattr(args, f"{prefix}_host", "")
    port = getattr(args, f"{prefix}_port")
    dbname = getattr(args, f"{prefix}_db")
    user = getattr(args, f"{prefix}_user")
    password = _resolve_password(
        getattr(args, f"{prefix}_password"),
        "PG_SOURCE_PASSWORD" if prefix == "source" else "PG_TARGET_PASSWORD",
        f"Password {prefix}: ",
    )

    if not host:
        raise ValueError(f"Falta --{prefix}-host o --{prefix}-url")

    return psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password,
        sslmode="require" if prefix == "target" else "prefer",
    )


def main() -> None:
    args = parse_args()
    excluded = [t for t in args.exclude.split(",")] if args.exclude else []

    source_conn = connect_from_args(args, "source")
    target_conn = connect_from_args(args, "target")
    source_conn.autocommit = True
    target_conn.autocommit = False

    try:
        source_tables = get_tables(source_conn, args.schema, excluded)
        target_tables = get_tables(target_conn, args.schema, [])
        tables, missing_in_target = intersect_tables(source_tables, target_tables)
        if missing_in_target and not args.dry_run:
            print(
                f"Creando tablas faltantes en destino ({len(missing_in_target)}): "
                + ", ".join(missing_in_target)
            )
            for table_name in missing_in_target:
                create_missing_table(source_conn, target_conn, args.schema, table_name)
            target_conn.commit()
            target_tables = get_tables(target_conn, args.schema, [])
            tables, missing_in_target = intersect_tables(source_tables, target_tables)

        if not tables:
            print("No se encontraron tablas para copiar.")
            return

        print(f"Tablas a copiar ({len(tables)}): {', '.join(tables)}")
        if missing_in_target:
            print(
                f"Tablas omitidas porque no existen en destino ({len(missing_in_target)}): "
                + ", ".join(missing_in_target)
            )
        if args.dry_run:
            print("Dry-run activado: no se escribió nada en destino.")
            return

        with target_conn.cursor() as cur:
            for table in tables:
                cur.execute(
                    sql.SQL("TRUNCATE TABLE {}.{} RESTART IDENTITY CASCADE").format(
                        sql.Identifier(args.schema),
                        sql.Identifier(table),
                    )
                )

        total_rows = 0
        for table in tables:
            cols = get_columns(source_conn, args.schema, table)
            rows_selected, rows_inserted = copy_table_data(
                source_conn, target_conn, args.schema, table, cols
            )
            total_rows += rows_inserted
            print(f"[OK] {table}: {rows_inserted}/{rows_selected} filas")

        target_conn.commit()
        print(f"\nSincronización completada. Filas copiadas: {total_rows}")
    except Exception:
        target_conn.rollback()
        raise
    finally:
        source_conn.close()
        target_conn.close()


if __name__ == "__main__":
    main()
