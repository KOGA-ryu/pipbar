# Invariants

This file defines the current pipeline invariants. Each invariant is intended to be explicit, testable, and limited to behavior that exists today.

## Run Count Invariants

- for completed runs, `rows_parsed == rows_valid + rows_invalid`
- `rows_valid == rows_inserted + rows_duplicates_skipped`
- all run counts are integers greater than or equal to zero
- `files_discovered >= 0`
- for failed runs, partial counts may exist before all parsed rows are classified
- for failed runs, persisted counts may reflect only files committed before the failure point

## Run Lifecycle And Status Invariants

- each pipeline execution that reaches run creation produces exactly one `import_runs` row for its `import_batch_id`
- a completed run has `status = "completed"`
- a failed run has `status = "failed"`
- completed and failed runs both have non-empty `started_at` and `completed_at`
- `running` is a start-state only and not the final persisted state for completed test paths

## Branching Invariants

- each parsed row in a tested run has one consistent fate
- row-level normalization failures become invalid rows rather than failed runs
- system-level failures still fail the run
- invalid rows are not inserted into `price_bars`
- invalid rows may be persisted to `rejected_rows`
- duplicate rows are not invalid rows
- duplicate rows are skipped during load and are not persisted to `rejected_rows`

## Database Invariants

- `price_bars` uniqueness is `(ticker, timeframe, ts)`
- `import_runs.import_batch_id` is one row per run
- `rejected_rows` stores original raw row payloads and issue lists as JSON text
- persistence is committed one file at a time in the runner
- all stored timestamps in the current pipeline contract are ISO-8601 UTC strings
