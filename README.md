pipbar
pipbar is a local data ingestion pipeline that converts raw stock CSV files into a validated, canonical, queryable dataset stored in SQLite.
It is designed to be:
* deterministic
* strict
* reproducible
* testable
* extensible
This is a pipeline system, not a parsing script.

What pipbar does
pipbar takes raw CSV market data and processes it through a staged pipeline:
discover → inspect → parse → normalize → validate → load → verify → report
Each stage has one responsibility:
* parse → read raw data
* normalize → convert to canonical schema
* validate → enforce correctness
* load → store valid records
* report → summarize results
Invalid data is never silently fixed.It is rejected with explicit reasons.

Core guarantees
pipbar enforces:
* Canonical schema — all data normalized before storage
* Strict validation — invalid rows are rejected, not repaired
* Duplicate safety — (ticker, timeframe, ts) uniquely identifies a record
* Idempotent runs — rerunning the same data is safe
* Traceability — every run is tracked
If data cannot be validated, it does not enter the system.

Project structure
The repository is organized by responsibility:
app/
  pipeline/   → stage implementations
  db/         → schema and SQL
  models/     → structured data objects
  rules/      → normalization and validation logic
  services/   → orchestration (import runner)

data/
  raw/        → input CSV files
  db/         → SQLite database

tests/
  fixtures/   → sample datasets
  *.py        → stage and pipeline tests

docs/
  contract.md
  roadmap.md
  decisions.md
Each module owns one job. No file exists “just in case.”

Getting started
1. Install dependencies
pip install -r requirements.txt
2. Initialize the database
python scripts/bootstrap_db.py
This creates the SQLite database from schema.sql.

3. Add input data
Place CSV files in:
data/raw/
For v1, expected format:
date,open,high,low,close,volume
Example file name:
aapl_1d.csv
Ticker is derived from filename in v1.

4. Run ingestion
python scripts/run_import.py

5. Verify output
Check the database:
* table: price_bars
* rows should match valid records from input
* rejected rows stored in rejected_rows

Example run output
batch_id: batch_20260319_234112
status: success

files_discovered: 1
files_processed: 1
files_failed: 0

rows_parsed: 10
rows_valid: 10
rows_rejected: 0

rows_inserted: 10
rows_duplicate_no_change: 0
rows_duplicate_updated: 0

Database schema (v1)
price_bars
Stores validated market data
Unique key:
(ticker, timeframe, ts)

import_runs
Tracks each pipeline execution

rejected_rows
Stores invalid input rows and reasons

Development roadmap
pipbar is built in phases:
1. Phase 1 — first vertical slice (single file ingestion)
2. Phase 2 — validation + rejection logging
3. Phase 3 — full staged pipeline
4. Phase 4 — duplicate-safe reruns
5. Phase 5 — run tracking
6. Phase 6 — test coverage
7. Phase 7 — hardening
See:
docs/roadmap.md

Design philosophy
pipbar follows strict data-engineering principles:
* do not guess
* do not auto-fix
* do not hide failure
* do not mix responsibilities
Good data systems are boring, predictable, and explainable.

Out of scope (v1)
pipbar intentionally does not include:
* feature engineering
* ML models
* APIs or web UI
* live data ingestion
* multi-source abstraction
These are future layers, not part of ingestion.

Why this exists
Most data pipelines fail quietly.
pipbar is built to make failure visible, enforce correctness, and produce data you can actually trust—especially for later analysis, backtesting, and ML workflows.

Next steps
* complete Phase 1 vertical slice
* validate behavior with fixtures
* harden validation and duplicate handling

If something behaves unexpectedly:check docs/contract.md before changing code.
That file defines what the system is allowed to do.


