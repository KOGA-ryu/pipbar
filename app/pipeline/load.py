from __future__ import annotations

import sqlite3

from app.db.queries import insert_price_bars
from app.models.price_bar import PriceBar


def load_valid_records(conn: sqlite3.Connection, records: list[PriceBar]) -> int:
    # Future optimization note:
    # batched prepared inserts are the first optimization path here.
    # consider a native extension only if profiling justifies it.
    inserted_count = insert_price_bars(conn, records)
    conn.commit()
    return inserted_count
