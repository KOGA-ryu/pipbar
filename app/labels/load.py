from __future__ import annotations

import sqlite3

from app.db.queries import insert_label_row, is_label_row_duplicate_error
from app.models.label_row import LabelRow


def load_label_rows(
    conn: sqlite3.Connection,
    rows: list[LabelRow],
) -> dict[str, int]:
    inserted_count = 0
    duplicate_count = 0

    for row in rows:
        try:
            insert_label_row(conn, row)
            inserted_count += 1
        except sqlite3.IntegrityError as error:
            if is_label_row_duplicate_error(error):
                duplicate_count += 1
                continue
            raise

    return {
        "rows_inserted": inserted_count,
        "rows_duplicates_skipped": duplicate_count,
    }
