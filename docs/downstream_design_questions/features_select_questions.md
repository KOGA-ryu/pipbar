# features/select.py Contract

## Purpose

`select.py` reads **trusted bars** for feature generation.

It queries `price_bars` and returns ordered `PriceBar` objects for downstream derivation.

This module is **read-only**:
- no feature computation
- no validation
- no writes

---

## Data source (first pass)

- `price_bars` only

No reading from feature or label tables in first slice.

---

## Supported filters (first pass)

- `ticker: str | None`
- `timeframe: str`
- `start_ts: str | None`
- `end_ts: str | None`
- `limit: int | None` (optional)

---

## Ordering contract

Output MUST be ordered by:

- `ts` ascending

Ordering is enforced here even if caller forgets.

---

## Output type

Returns:

```
list[PriceBar]
```

No raw dicts, no SQLite rows.

---

## Minimum function signature

```python
select_bars(
    db_path: str,
    ticker: str | None,
    timeframe: str,
    start_ts: str | None,
    end_ts: str | None,
    limit: int | None = None,
) -> list[PriceBar]
```

---

## Input validation ownership

- `timeframe` is required
- invalid parameters raise immediately

Runner is responsible for higher-level orchestration validation.

---

## Contiguity and gaps

- gaps in bar sequences are **not filled** here
- missing timestamps are passed through as-is

Handling gaps is downstream responsibility (typically `derive.py`).

---

## Warmup policy (first pass)

- no warmup logic in `select.py`
- no lookback expansion

Future rolling features may require extended selection, but not in this slice.

---

## Empty result behavior

- empty selection is valid
- returns `[]`
- does not raise

"No bars found" is not an error.

---

## Responsibility boundaries

`select.py`:
- queries `price_bars`
- applies filters
- enforces ordering
- returns typed rows

It does **not**:
- compute features
- read feature tables
- read label tables
- join datasets
- validate rows

---

## Determinism

Given the same DB state and inputs, output must be identical.

---

## Summary

This module answers:

> "Which ordered bars should be used for feature derivation?"

Nothing more.
