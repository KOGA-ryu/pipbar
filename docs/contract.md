# `contract.md` — pipbar

## Purpose

pipbar is a local stock data ingestion pipeline that converts raw CSV market data into a **validated, canonical, queryable dataset** stored in SQLite.

The system enforces strict data contracts to ensure:

* deterministic transformations
* reproducible runs
* auditable failures
* duplicate-safe storage

This is a **data pipeline**, not a script.

---

## System Principles

* **Deterministic**: same input → same output
* **Strict**: invalid data is rejected, not repaired
* **Transparent**: all failures are logged with reasons
* **Idempotent**: rerunning imports does not corrupt data
* **Stage-based**: each step has one responsibility

---

## Canonical Record Definition

Each row represents one market bar:

**Identity**

```
(ticker, timeframe, ts)
```

**Schema**

```
ticker: string (uppercase, required)
timeframe: string (v1 = "1d")
ts: ISO-8601 UTC datetime (required)

open: float (>= 0, required)
high: float (>= 0, required)
low: float (>= 0, required)
close: float (>= 0, required)
volume: integer (>= 0, required)

source: string (required)
import_batch_id: string (required)
```

All records must conform to this schema before storage.

---

## Pipeline Stages

The system processes data through explicit stages:

```
discover → inspect → parse → normalize → validate → load → verify → report
```

Each stage:

* accepts structured input
* produces structured output
* does one job only

Key rules:

* **parse** = read structure
* **normalize** = transform into canonical schema
* **validate** = enforce truth rules
* **load** = persist only valid data

No stage performs another stage’s responsibility. 

---

## Validation Contract

A record is valid only if:

### Required fields

* ticker, timeframe, ts, open, high, low, close, volume must exist

### Type and value rules

* numeric fields must be valid numbers
* volume must be integer
* all numeric values ≥ 0

### Logical rules

* high ≥ low
* low ≤ open ≤ high
* low ≤ close ≤ high

### Behavior

* invalid rows are rejected
* no silent fixes
* multiple issues per row are allowed
* all rejections must include explicit issue codes

---

## Duplicate Policy

Uniqueness is enforced by:

```
UNIQUE (ticker, timeframe, ts)
```

Behavior:

* new key → insert
* same key, same values → no-op
* same key, different values → update existing row

The pipeline must be **idempotent**:

* rerunning the same data must not create duplicates

Duplicates are handled during **load**, not validation.

---

## Run Model

A **run** is one execution of the pipeline.

Each run:

* generates a single `import_batch_id`
* processes files in deterministic order
* accumulates structured metrics
* produces a final summary

Tracked fields include:

* files processed
* rows parsed
* rows valid / rejected
* rows inserted / updated / skipped

Run statuses:

* `success`
* `partial_success`
* `failed`
* `success_no_files`

Runs must be reproducible and traceable.

---

## Database Tables

### `price_bars`

Stores validated canonical records

* enforces uniqueness `(ticker, timeframe, ts)`
* contains latest known values

---

### `import_runs`

Stores run-level metadata

* one row per pipeline execution
* includes counters and status

---

### `rejected_rows`

Stores invalid input data

* includes raw row
* includes normalized attempt
* includes issue list

---

Design principle:

> Store canonical data, run metadata, and failure evidence.
> Nothing else is required for v1.

---

## Repository Structure

The repository is organized by responsibility:

* `pipeline/` → stage implementations
* `db/` → schema and SQL
* `models/` → structured data objects
* `rules/` → transformation and validation logic
* `services/` → orchestration
* `tests/` → verification
* `docs/` → contracts and decisions

Each module owns one job.
No file exists “just in case.” 

---

## Implementation Contract

Development follows phased construction:

* Phase 0: scaffold + contracts
* Phase 1: first vertical slice
* Phase 2: validation hardening
* Phase 3: duplicate-safe reruns
* Phase 4: run tracking
* Phase 5: polish + extensions

The first working version must prove:

* one CSV → full pipeline → SQLite
* no stage bypassing
* correct schema output
* valid rows inserted
* invalid rows rejected

Build order and file responsibilities are defined explicitly.  

---

## Non-Goals (v1)

* no live data ingestion
* no ML or feature engineering
* no UI
* no multi-provider abstraction
* no schema evolution system
* no data correction logic

---

## Final Rule

If data cannot be:

* explained
* reproduced
* validated

then it does not belong in the system.

---

## What you just built

This isn’t just a doc.

This is:

* a spec
* a guardrail
* a debugging tool
* and your future sanity

