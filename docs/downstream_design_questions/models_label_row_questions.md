# models/label_row.py Contract

## Purpose

`label_row.py` defines the **typed label row shape** used by the label pipeline.

It represents one supervised target attached to a canonical bar.

This model is a **plain typed container**:
- no SQL
- no export helpers
- no orchestration logic

---

## First-pass row grain

Each `LabelRow` represents exactly:

```text
one (ticker, timeframe, ts)
```

This MUST match the grain of `price_bars`.

---

## Required fields

Every `LabelRow` MUST include:

- `ticker: str`
- `timeframe: str`
- `ts: str`

These identifiers are mandatory and non-null.

---

## First-pass label fields

Include only:

- `next_1d_return: float | None`

This field represents the future return from `t` to `t+1`.

---

## Nullability rules

- `next_1d_return` may be `None` only for tail rows (no future bar)

All identifier fields must be non-null.

---

## Batch tracking

Include:

- `label_batch_id: str`

This is required for traceability.

---

## Horizon metadata

Horizon length (e.g. 1-bar lookahead) does NOT belong in the row.

It is defined by:
- the label contract
- the runner configuration

---

## Method policy

`LabelRow` must remain method-free.

It is a data container only.

---

## Width policy

First pass keeps `LabelRow` minimal:

- identifiers
- label value
- batch id

Do not add:
- feature values
- split flags
- export metadata
- model predictions

---

## Output role

`LabelRow` is used by:
- `labels/derive.py`
- `labels/validate.py`
- `labels/load.py`
- `datasets/select.py`

It must remain stable and predictable.

---

## Determinism

Given identical input bars, the same label rows must be produced.

---

## Responsibility boundaries

`label_row.py`:
- defines row shape only

It does **not**:
- derive labels
- validate rows
- persist data
- know about dataset splits

---

## Summary

This model answers:

> "What is the exact typed row shape for a supervised label attached to a bar?"

Nothing more.
