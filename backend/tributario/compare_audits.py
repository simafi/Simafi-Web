"""
Comparar dos auditorías JSON generadas por `db_audit.py`.

Uso:
  python backend/tributario/compare_audits.py mysql_audit.json pg_audit.json > diff.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def _load(path: str) -> dict:
    raw = Path(path).read_bytes()
    enc = "utf-16" if raw[:2] in (b"\xff\xfe", b"\xfe\xff") else "utf-8"
    return json.loads(raw.decode(enc))


def _colset(tinfo: dict) -> set[str]:
    cols = tinfo.get("columns") or []
    return {c.get("name") for c in cols if isinstance(c, dict) and c.get("name")}


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: compare_audits.py <audit1.json> <audit2.json>", file=sys.stderr)
        return 2

    a = _load(sys.argv[1])
    b = _load(sys.argv[2])

    a_tables: dict = a.get("tables") or {}
    b_tables: dict = b.get("tables") or {}

    a_set = set(a_tables.keys())
    b_set = set(b_tables.keys())

    only_a = sorted(a_set - b_set)
    only_b = sorted(b_set - a_set)
    both = sorted(a_set & b_set)

    col_diff = {}
    for t in both:
        ac = _colset(a_tables[t])
        bc = _colset(b_tables[t])
        if ac != bc:
            col_diff[t] = {
                "only_in_a": sorted(ac - bc),
                "only_in_b": sorted(bc - ac),
            }

    out = {
        "a": {"db_vendor": a.get("db_vendor"), "db_name": a.get("db_name")},
        "b": {"db_vendor": b.get("db_vendor"), "db_name": b.get("db_name")},
        "tables": {
            "only_in_a": only_a,
            "only_in_b": only_b,
            "column_differences": col_diff,
        },
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

