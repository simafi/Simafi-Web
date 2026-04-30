import collections
import json
import pathlib


def load_audit(path: str) -> dict:
    p = pathlib.Path(path)
    raw = p.read_bytes()
    enc = "utf-16" if raw[:2] in (b"\xff\xfe", b"\xfe\xff") else "utf-8"
    return json.loads(raw.decode(enc))


def main() -> None:
    d = load_audit("mysql_audit.json")
    tabs = d["tables"]

    empty = sorted([t for t, v in tabs.items() if v.get("rowcount", 0) == 0])
    non = [(t, v.get("rowcount", 0)) for t, v in tabs.items() if v.get("rowcount", 0) > 0]
    non.sort(key=lambda x: x[1], reverse=True)

    known = [
        "tributario",
        "tributario_app",
        "cont",
        "presu",
        "sp",
        "teso",
        "compras",
        "catastro",
        "mod",
        "auth",
        "django",
        "adm",
        "audit",
    ]
    g: dict[str, list[str]] = collections.defaultdict(list)
    for t in empty:
        hit = None
        for k in known:
            if t.startswith(k + "_") or t == k:
                hit = k
                break
        g[hit or "other"].append(t)

    out_lines: list[str] = []
    out_lines.append(f"tables_total: {len(tabs)}")
    out_lines.append(f"empty_tables: {len(empty)}")
    out_lines.append("")
    for k in known + ["other"]:
        if k in g:
            out_lines.append(f"## {k}: {len(g[k])}")
            out_lines.extend(g[k])
            out_lines.append("")
    pathlib.Path("mysql_empty_by_module.txt").write_text("\n".join(out_lines), encoding="utf-8")

    summary = {
        "db_vendor": d.get("db_vendor"),
        "db_name": d.get("db_name"),
        "tables_total": len(tabs),
        "empty_tables_total": len(empty),
        "empty_tables_by_group": {k: len(v) for k, v in g.items()},
        "top_nonempty_tables": [{"table": t, "rowcount": c} for t, c in non[:50]],
    }
    pathlib.Path("mysql_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("Wrote mysql_empty_by_module.txt and mysql_summary.json")


if __name__ == "__main__":
    main()

