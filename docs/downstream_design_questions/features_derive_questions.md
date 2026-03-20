# features/derive.py Contract

## Purpose

`derive.py` computes **deterministic feature values** from ordered `PriceBar` sequences.

This module is **math-only**:
- no SQL
- no file I/O
- no orchestration
- no side effects

---

## First-pass features (locked)

- `close_open_delta = close - open`
- `high_low_range = high - low`
- `close_1d_return = (close_t / close_t-1) - 1`

All outputs are **decimal ratios**, not percentages.

---

## Input requirements

- input is **ordered bars** per `(ticker, timeframe)` by `ts` ascending
- function receives bars only (no DB access)

---

## Lookback policy (first pass)

- only `close_1d_return` requires lookback (1 prior bar)
- same-bar features (`delta`, `range`) require no history

---

## Timestamp alignment

All feature rows are aligned to **current bar timestamp (`ts`)**.

---

## Missing history behavior

For rows lacking required history (first row per series):

- emit row with `close_1d_return = None`
- do not drop row
- do not raise

---

## Division-by-zero behavior

If `close_t-1 == 0`:

- set `close_1d_return = None`
- do not raise

---

## Output type

Returns:

```
list[PriceBarFeature]
```

Each row includes:
- identifiers (`ticker`, `timeframe`, `ts`)
- feature columns

---

## Determinism

Feature derivation MUST be:

- deterministic
- pure
- repeatable

Same input → same output.

---

## Responsibility boundaries

`derive.py`:
- computes feature values

Does NOT:
- query SQL
- validate rows
- persist data
- split datasets
- train models

---

## Minimal function signature

```python
compute_features(bars: list[PriceBar]) -> list[PriceBarFeature]
```

No extra parameters in first pass.

---

## Explicitly out of scope (first slice)

- rolling windows (SMA, EMA, ATR, etc.)
- multi-bar volatility measures
- cross-ticker features
- normalization/scaling
- label generation

---

## Summary

This module answers:

> "Given ordered bars, what deterministic feature values can we compute per row?"

Nothing more.
