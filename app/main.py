from __future__ import annotations

import sys
from pathlib import Path

from app.services.import_runner import run_import

DEFAULT_INPUT_DIR = "tests/fixtures"
DEFAULT_DB_PATH = "data/db/stock_data.sqlite3"
DEFAULT_SCHEMA_PATH = "app/db/schema.sql"
DEFAULT_IMPORT_BATCH_ID = "phase1-run"


def main() -> None:
    input_dir = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_INPUT_DIR

    Path(DEFAULT_DB_PATH).parent.mkdir(parents=True, exist_ok=True)

    run_import(
        input_dir=input_dir,
        db_path=DEFAULT_DB_PATH,
        schema_path=DEFAULT_SCHEMA_PATH,
        import_batch_id=DEFAULT_IMPORT_BATCH_ID,
    )


if __name__ == "__main__":
    main()
