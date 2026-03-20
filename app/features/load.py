from __future__ import annotations

import sqlite3

from app.db.queries import (
    insert_price_bar_feature,
    is_price_bar_feature_duplicate_error,
)
from app.models.price_bar_feature import PriceBarFeature


def load_feature_rows(
    conn: sqlite3.Connection,
    rows: list[PriceBarFeature],
) -> dict[str, int]:
    inserted_count = 0
    duplicate_count = 0

    for row in rows:
        try:
            insert_price_bar_feature(conn, row)
            inserted_count += 1
        except sqlite3.IntegrityError as error:
            if is_price_bar_feature_duplicate_error(error):
                duplicate_count += 1
                continue
            raise

    return {
        "rows_inserted": inserted_count,
        "rows_duplicates_skipped": duplicate_count,
    }
