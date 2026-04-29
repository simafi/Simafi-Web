# -*- coding: utf-8 -*-
"""Utilidades Postgres/Supabase para tablas cuyo `id` perdió secuencia tras importación."""
from django.db import connection


def assign_pk_if_postgres_serial_missing(table_name: str, instance) -> None:
    """
    Si `id` no tiene DEFAULT con nextval, asigna MAX(id)+1 antes del INSERT.
    No-op en no-Postgres o si el registro ya tiene pk.
    """
    if connection.vendor != "postgresql":
        return
    if not instance._state.adding or instance.pk is not None:
        return
    qtable = connection.ops.quote_name(table_name)
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT COALESCE(column_default, '')
            FROM information_schema.columns
            WHERE table_schema = 'public'
              AND table_name = %s
              AND column_name = 'id'
            """,
            [table_name],
        )
        row = cursor.fetchone()
        default = (row[0] or "") if row else ""
        if "nextval" in default.lower():
            return
        cursor.execute(f"SELECT COALESCE(MAX(id), 0) + 1 FROM {qtable}")
        instance.pk = int(cursor.fetchone()[0])
