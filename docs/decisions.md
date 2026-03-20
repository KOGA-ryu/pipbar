# `decisions.md` — pipbar

## Purpose

This file records key design decisions made during development.

It exists to:

* prevent re-litigating past choices
* preserve system intent
* make future changes deliberate instead of accidental

If something feels “weird,” check here before changing it.

---

## Core Philosophy

### Decision: Build a pipeline, not a script

**Why:**
Scripts collapse parsing, validation, and storage into one blob.
Pipelines enforce separation of concerns and make failures visible.

**Impact:**

* explicit stages
* easier debugging
* reusable components
* ML-ready structure later

---

### Decision: Strict over permissive

**Why:**
“Helpful” systems silently corrupt data.

**Choice:**

* invalid data is rejected, not repaired
* missing values are not guessed
* ambiguous data is surfaced, not inferred

**Impact:**

* fewer hidden bugs
* higher trust dataset
* easier ML transition

---

## Data Design Decisions

### Decision: Canonical schema first

**Why:**
Without one schema, the system fragments immediately.

**Choice:**
All data must normalize into:

* ticker
* timeframe
* ts
* OHLCV

before it is considered valid.

**Impact:**

* consistent downstream queries
* simpler validation
* stable storage

---

### Decision: Timeframe included from day one

**Why:**
Most people regret not doing this immediately.

**Choice:**
Even though v1 only uses `"1d"`, the field exists.

**Impact:**

* no schema rewrite when adding intraday data
* clean extensibility

---

### Decision: UTC timestamps only

**Why:**
Timezone bugs are subtle and destructive.

**Choice:**
All timestamps normalized to ISO-8601 UTC.

**Impact:**

* consistent comparisons
* no DST issues
* easier ML dataset alignment

---

### Decision: All OHLCV required in v1

**Why:**
Partial records introduce ambiguity.

**Choice:**

* no missing OHLCV values allowed
* rows missing any required field are rejected

**Impact:**

* cleaner dataset
* simpler logic
* stronger validation discipline

---

## Pipeline Design Decisions

### Decision: Explicit staged pipeline

**Stages:**

```text
discover → inspect → parse → normalize → validate → load → verify → report
```

**Why:**
Each stage answers one question.

**Impact:**

* testable units
* easier debugging
* reusable pipeline structure

---

### Decision: Do not combine stages

**Why:**
Mixing responsibilities leads to hidden bugs.

**Examples:**

* parse does not normalize
* normalize does not validate
* validate does not load

**Impact:**

* clarity
* maintainability
* predictable behavior

---

## Validation Decisions

### Decision: Validation after normalization only

**Why:**
You cannot validate inconsistent raw formats.

**Choice:**

* raw → normalize → validate
* never validate raw strings

---

### Decision: Reject, don’t repair

**Why:**
Auto-fixing hides real problems.

**Choice:**

* high < low → reject
* negative prices → reject
* invalid timestamp → reject

**Impact:**

* data integrity preserved
* errors visible

---

### Decision: Multiple issues per row

**Why:**
Single-error reporting hides full failure context.

**Impact:**

* better debugging
* better analytics later

---

## Duplicate Handling Decisions

### Decision: Upsert-based duplicate policy

**Behavior:**

* new → insert
* same → no-op
* changed → update

**Why:**

* supports reruns
* supports corrected data
* prevents duplication

---

### Decision: Identity = (ticker, timeframe, ts)

**Why:**
This uniquely defines a market bar.

**Impact:**

* consistent dedupe logic
* stable database constraints

---

### Decision: Database enforces uniqueness

**Why:**
Python checks are not enough.

**Choice:**
Use SQL `UNIQUE` constraint.

**Impact:**

* guaranteed integrity
* prevents silent duplication

---

## Run Model Decisions

### Decision: One batch per run

**Why:**
Simplest traceability model.

**Choice:**

* one `import_batch_id` per run
* applied to all rows

**Impact:**

* easy debugging
* clean audit trail

---

### Decision: Runs are idempotent

**Why:**
Pipelines must be safe to rerun.

**Impact:**

* no duplicate buildup
* reproducible results

---

### Decision: File failures are isolated

**Why:**
One bad file should not block all progress.

**Choice:**

* continue processing other files
* mark run as partial success

---

## Storage Decisions

### Decision: SQLite for v1

**Why:**

* simple
* local
* zero setup
* good enough

**Impact:**

* fast iteration
* easy debugging

---

### Decision: Minimal table set

Tables:

* `price_bars`
* `import_runs`
* `rejected_rows`

**Why:**
Avoid premature complexity.

---

### Decision: Store rejected rows

**Why:**
Silent failure destroys debuggability.

**Impact:**

* full audit trail
* easier debugging
* future anomaly analysis

---

### Decision: Raw files stay untouched

**Why:**
Raw data is the source of truth.

**Choice:**

* no automatic file movement in v1

**Impact:**

* reproducibility
* easier debugging

---

## Implementation Decisions

### Decision: Build vertical slice first

**Why:**
Proves system works end-to-end.

**Impact:**

* faster feedback
* less overengineering

---

### Decision: One known CSV format first

**Why:**
Multi-format parsing explodes complexity.

**Impact:**

* faster progress
* clearer debugging

---

### Decision: Hardcode early assumptions

Examples:

* timeframe = `"1d"`
* source = `"massive_csv"`
* ticker from filename

**Why:**
Reduce early branching complexity.

---

### Decision: Minimal abstraction first

**Why:**
Premature abstraction hides logic.

**Choice:**

* simple functions
* explicit transformations
* refactor later

---

## Testing Decisions

### Decision: Fixture-driven tests

**Why:**
Data systems need real input examples.

**Fixtures include:**

* valid data
* missing fields
* invalid OHLC
* duplicates

---

### Decision: End-to-end test required early

**Why:**
Proves pipeline actually works.

---

## Things Deliberately Not Done (Yet)

* feature engineering
* ML integration
* live data ingestion
* schema versioning
* parquet export
* multi-source abstraction
* UI

These are not forgotten.
They are postponed intentionally.

---

## Final Rule

If a change:

* weakens validation
* hides failure
* breaks reproducibility

it is probably wrong.

---

## Future Use

Before changing:

* schema
* validation rules
* duplicate policy
* pipeline stages

Check this file.

If the reason for the change is not stronger than the original decision, do not change it.

---

This file will save you from:

* overengineering
* regression bugs
* forgetting why things were strict


