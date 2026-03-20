# pipbar — roadmap.md

## Purpose

This roadmap defines the build order for v1 of pipbar.

The goal is to build a working ingestion pipeline early, then harden it in controlled layers without breaking the system contract.

This roadmap follows the locked design:
- one canonical schema
- one staged pipeline
- one duplicate policy
- one run model
- three core DB tables

Every phase must leave the project in a runnable, more trustworthy state than before.

---

## Current Status

### Phase 0 — Skeleton
Status: complete

The repository skeleton, module layout, and base documentation have already been created.

Completed foundation:
- repo structure
- module placeholders
- docs structure
- database schema file
- requirements file
- README foundation

Phase 0 is finished. Do not reopen it unless structure is actually broken.

---

## Phase 1 — First Vertical Slice

### Goal

Prove the real pipeline works end-to-end on one known-good daily CSV format.

### Scope

Implement only what is required to move one valid CSV file through the actual system path:

discover → parse → normalize → validate → load → report

### Build

Core files:
- `app/db/connection.py`
- `app/db/init_db.py`
- `app/db/queries.py`
- `app/models/price_bar.py`
- `app/pipeline/discover.py`
- `app/pipeline/parse.py`
- `app/pipeline/normalize.py`
- `app/pipeline/validate.py`
- `app/pipeline/load.py`
- `app/pipeline/report.py`
- `app/services/import_runner.py`
- `app/main.py`

Test fixture:
- `tests/fixtures/aapl_1d.csv`

Test:
- `tests/test_pipeline.py`

### Locked assumptions

- one file format only
- daily bars only
- ticker derived from filename
- timeframe hardcoded to `"1d"`
- source hardcoded to `"massive_csv"`
- no advanced duplicate handling yet beyond clean insert path
- no run-table persistence required yet if it slows the slice down

### Exit Criteria

- database initializes from `schema.sql`
- fixture file is discovered
- rows are parsed into raw row structures
- rows normalize into canonical records
- rows pass strict validation
- rows insert into `price_bars`
- terminal summary prints correct counts
- one end-to-end test passes

---

## Phase 2 — Validation and Rejection Logging

### Goal

Make the system trustworthy on bad data, not just functional on good data.

### Build

- harden `app/pipeline/validate.py`
- implement `app/models/rejected_row.py`
- connect `rejected_rows` table writes
- add focused validation helpers, either in `validate.py` first or later in `rules/validation_rules.py`

### Add validation coverage

- required fields
- numeric coercion failures
- non-negative OHLCV checks
- OHLC relationship checks
- explicit issue lists

### Add fixtures

- `tests/fixtures/missing_field.csv`
- `tests/fixtures/invalid_ohlc.csv`

### Exit Criteria

- invalid rows never enter `price_bars`
- rejected rows are stored with reasons
- valid rows still load correctly
- validation failures are reproducible in tests

---

## Phase 3 — Full Staged Pipeline

### Goal

Activate the complete staged flow and keep responsibilities clean.

### Build

- `app/pipeline/inspect.py`
- `app/pipeline/verify.py`
- fuller `app/pipeline/report.py`
- strengthen `app/services/import_runner.py`

### Full flow

discover → inspect → parse → normalize → validate → load → verify → report

### Notes

This phase is about making the architecture honest, not fancy.

`main.py` stays thin.  
`import_runner.py` orchestrates.  
Stage modules own their own jobs. :contentReference[oaicite:2]{index=2}

### Exit Criteria

- folder of CSV files can be processed end-to-end
- stage boundaries remain clean
- verification checks basic expectations after load
- run summary is accurate

---

## Phase 4 — Duplicate Policy and Safe Reruns

### Goal

Make reruns safe and deterministic.

### Build

- duplicate detection in `load.py`
- supporting queries in `db/queries.py`
- SQL behavior aligned with unique key:
  - `(ticker, timeframe, ts)`

### Policy

- new key → insert
- same key, same values → no-op
- same key, different values → update

### Exit Criteria

- rerunning the same file does not duplicate rows
- exact duplicates are counted as no-op
- conflicting duplicates update consistently
- duplicate behavior is covered by tests

---

## Phase 5 — Run Tracking

### Goal

Make each import execution traceable.

### Build

- `app/models/import_run.py`
- `app/services/batch_id.py`
- `import_runs` table writes
- batch lifecycle in `import_runner.py`

### Track

- run id / batch id
- start time
- end time
- files discovered
- files processed
- files failed
- rows parsed
- rows valid
- rows rejected
- rows inserted
- duplicate no-change count
- duplicate updated count
- final status

### Exit Criteria

- each run is recorded in `import_runs`
- metrics are accurate
- reruns remain safe
- run summaries match database state

---

## Phase 6 — Focused Test Coverage

### Goal

Make failures reproducible and expected behavior provable.

### Fixtures

- `valid_daily.csv`
- `missing_field.csv`
- `invalid_ohlc.csv`
- `duplicate_rows.csv`

### Tests

- `test_discover.py`
- `test_parse.py`
- `test_normalize.py`
- `test_validate.py`
- `test_load.py`
- `test_pipeline.py`

### Exit Criteria

- each core stage has at least one focused test
- end-to-end test passes
- duplicate handling is covered
- rejection behavior is covered

---

## Phase 7 — Hardening

### Goal

Stabilize pipbar for repeated real use.

### Add

- better error handling
- cleaner logging
- path handling cleanup
- config cleanup
- removal of dead helpers
- module-boundary cleanup

### Exit Criteria

- malformed files do not crash the whole run
- logs are readable and useful
- module ownership still matches contract
- no major logic drift from original design

---

## Out of Scope for v1

Do not add these during v1:

- feature engineering
- ML training
- APIs
- web UI
- plugin systems
- multi-source ingestion
- distributed processing
- heavy config frameworks
- speculative abstractions

These are postponed intentionally, not forgotten.

---

## Final Definition of Done (v1)

pipbar v1 is complete when:

- CSV files can be ingested reliably
- canonical records are stored in SQLite
- invalid rows are rejected and logged
- duplicates are handled safely
- runs are tracked
- pipeline stages remain cleanly separated
- tests prove core behavior

---

## Guiding Constraint

Every phase must produce a working system.

No phase should introduce:
- unused abstraction
- speculative features
- cross-module leakage
- structure that exists only for appearances

If a feature is not required for the current phase, it does not get built.