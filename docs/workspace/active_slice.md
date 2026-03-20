# Active Slice

This file defines the current focused working set without changing the full repo layout.

## Focused Workspace

- active snapshot path: `/tmp/pipbar-focus`

## Active Code Files

- `app/main.py`
- `app/db/connection.py`
- `app/db/init_db.py`
- `app/db/queries.py`
- `app/db/schema.sql`
- `app/models/price_bar.py`
- `app/pipeline/discover.py`
- `app/pipeline/parse.py`
- `app/pipeline/normalize.py`
- `app/pipeline/validate.py`
- `app/pipeline/load.py`
- `app/pipeline/report.py`
- `app/services/import_runner.py`

## Active Test Files

- `tests/test_pipeline.py`
- `tests/test_validation_failures.py`
- `tests/test_normalize.py`
- `tests/test_load_integrity.py`
- `tests/test_discover.py`

## Active Fixtures

- `tests/fixtures/valid_daily.csv`
- `tests/fixtures/invalid_ohlc.csv`
- `tests/fixtures/invalid_negative_values.csv`
- `tests/fixtures/invalid_missing_fields.csv`

## Notes

- the full repo remains the source archive
- the focused snapshot is for cleaner day-to-day work on the active slice only
- when the active slice changes, refresh the snapshot intentionally rather than letting it drift
