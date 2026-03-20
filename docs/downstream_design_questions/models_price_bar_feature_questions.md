# models/price_bar_feature.py Contract

## Purpose

`price_bar_feature.py` defines the **typed feature row shape** produced by the feature pipeline.

It represents one set of derived feature values aligned to a canonical bar.

This model is a **plain typed container**:
- no SQL
- no export helpers
- no orchestration logic

---

## First-pass row grain

Each `PriceBarFeature` represents exactly:

```text
one (ticker, timeframe, ts)
```

This MUST match the grain of `price_bars`.

---

## Required identifier fields

Every `PriceBarFeature` MUST include:

- `ticker: str`
- `timeframe: str`
- `ts: str`

These identifiers are mandatory and non-null.

---

## First-pass feature fields

Include only:

- `close_1d_return: float | None`
- `high_low_range: float | None`
- `close_open_delta: float | None`

These fields may be `None` only where upstream feature contract allows it (warmup behavior).

---

## Nullability rules

- feature values may be `None` only for valid warmup conditions
- identifiers must never be null

---

## Batch tracking

Include:

- `feature_batch_id: str`

This is required for traceability.

---

## Timestamp ownership

`created_at` does **not** belong in the dataclass.

Reason:
- persistence layer owns insertion time
- model should represent logical row, not storage metadata

---

## Method policy

`PriceBarFeature` must remain method-free.

No helpers like:
- `to_db_tuple()`
- serialization helpers

All DB shaping belongs in `db/queries.py`.

---

## Width policy

First pass keeps `PriceBarFeature` minimal:

- identifiers
- feature values
- batch id

Do not add:
- raw bar values
- label values
- split flags
- export metadata
- model predictions

---

## Output role

`PriceBarFeature` is used by:

- `features/derive.py`
- `features/validate.py`
- `features/load.py`
- `datasets/select.py`

It must remain stable and predictable.

---

## Determinism

Given identical input bars, the same feature rows must be produced.

---

## Responsibility boundaries

`price_bar_feature.py`:
- defines row shape only

It does **not**:
- compute features
- validate rows
- persist data
- know about dataset assembly

---

## Summary

This model answers:

> "What is the exact typed row shape for derived features aligned to a bar?"

Nothing more.
