# features/validate.py Contract

## Purpose

`validate.py` enforces **feature row integrity** after derivation.

It determines which feature rows are acceptable for persistence and which should be excluded.

This module is **judgment-only**:
- no feature computation
- no SQL
- no orchestration

---

## First-pass validation scope

Validation enforces:

- structural correctness
- basic numeric sanity

It does NOT enforce:
- statistical properties
- feature distributions
- advanced domain constraints

---

## Required fields

Every feature row MUST include:

- `ticker`
- `timeframe`
- `ts`

These must be non-null.

---

## Feature column rules (first pass)

Allowed values:

- float values
- `None` (only for warmup-related fields)

Disallowed values:

- `NaN`
- `inf`
- `-inf`

---

## Warmup behavior

Warmup-related `None` values are **allowed**.

Example:
- `close_1d_return = None` for first row

These rows are **valid**, not rejected.

---

## Invalid row conditions

A feature row is invalid if:

- required identifiers are missing
- numeric fields contain `NaN` or infinite values
- feature row structure is malformed

---

## Structural vs data insufficiency

Validation must distinguish:

- **invalid row** → bad structure or illegal numeric values
- **insufficient history** → valid row with `None` values

Only invalid rows are rejected.

---

## Issue messages

First-pass issue messages must be stable and explicit:

- `missing required field`
- `invalid numeric value`
- `malformed feature row`

No free-form error strings.

---

## Output contract

Return a structured result:

```text
FeatureValidationResult:
  valid_rows: list[PriceBarFeature]
  invalid_rows: list[dict]
```

Each invalid row includes:

- original feature row
- issue list

---

## Rejected feature rows (first pass)

Rejected feature rows are **not persisted**.

They are:

- counted
- surfaced in summary

Persistence may be added later.

---

## Responsibility boundaries

`validate.py`:
- evaluates feature rows
- separates valid and invalid rows

It does **not**:
- compute features
- query database
- persist data
- generate labels

---

## Determinism

Given identical input rows, output must be identical.

---

## Summary

This module answers:

> "Which derived feature rows are structurally valid and safe to persist?"

Nothing more.
