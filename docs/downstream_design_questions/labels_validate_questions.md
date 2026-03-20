# labels/validate.py Contract

## Purpose

`validate.py` enforces **label row integrity** after derivation.

It determines which label rows are acceptable for persistence and which should be excluded.

This module is **judgment-only**:
- no label derivation
- no SQL
- no orchestration

---

## First-pass validation scope

Validation enforces:

- structural correctness
- basic numeric sanity

It does NOT enforce:
- model assumptions
- feature-label relationships
- statistical properties

---

## Required fields

Every label row MUST include:

- `ticker`
- `timeframe`
- `ts`

These must be non-null.

---

## Label value rules (first pass)

Allowed values:

- float values
- `None` (only for tail rows without future data)

Disallowed values:

- `NaN`
- `inf`
- `-inf`

---

## Tail-row behavior

Tail rows without future outcome are **valid**.

Example:
- `next_1d_return = None`

These rows are not rejected.

---

## Invalid row conditions

A label row is invalid if:

- required identifiers are missing
- numeric fields contain `NaN` or infinite values
- row structure is malformed

---

## Structural vs data insufficiency

Validation must distinguish:

- **invalid row** → malformed or illegal numeric values
- **expected missing outcome** → valid row with `None`

Only invalid rows are rejected.

---

## Issue messages

First-pass issue messages must be stable and explicit:

- `missing required field`
- `invalid numeric value`
- `malformed label row`

No free-form error strings.

---

## Output contract

Return a structured result:

```text
LabelValidationResult:
  valid_rows: list[LabelRow]
  invalid_rows: list[dict]
```

Each invalid row includes:

- original label row
- issue list

---

## Rejected label rows (first pass)

Rejected label rows are **not persisted**.

They are:

- counted
- surfaced in summary

Persistence may be added later.

---

## Leakage awareness

`validate.py` does NOT inspect dataset splits.

Leakage prevention is handled by:
- label derivation rules
- dataset splitting

---

## Responsibility boundaries

`validate.py`:
- evaluates label rows
- separates valid and invalid rows

It does **not**:
- derive labels
- query database
- persist data
- inspect feature values
- inspect dataset splits

---

## Determinism

Given identical input rows, output must be identical.

---

## Summary

This module answers:

> "Which derived label rows are structurally valid and safe to persist?"

Nothing more.
