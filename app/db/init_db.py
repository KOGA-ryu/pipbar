from __future__ import annotations

from pathlib import Path

from app.db.connection import get_connection


def init_db(db_path: str, schema_path: str) -> None:
    schema_sql = Path(schema_path).read_text(encoding="utf-8")
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    with get_connection(db_path) as connection:
        connection.executescript(schema_sql)
