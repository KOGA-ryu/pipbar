# Feature Table Contract

This document locks the first-pass `price_bar_features` table contract.

It exists so the next feature code batch does not invent schema details mid-build.

## Table Purpose

`price_bar_features` stores deterministic derived values at the same grain as `price_bars`.

One row represents:

```text
(ticker, timeframe, ts)
```

This table is downstream of `price_bars` and upstream of labels and dataset assembly.

## First-Pass Columns

Required columns:

- `id INTEGER PRIMARY KEY AUTOINCREMENT`
- `ticker TEXT NOT NULL`
- `timeframe TEXT NOT NULL`
- `ts TEXT NOT NULL`
- `close_1d_return REAL`
- `high_low_range REAL NOT NULL`
- `close_open_delta REAL NOT NULL`
- `feature_batch_id TEXT NOT NULL`
- `created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))`

## Nullability Rules

Nullable:

- `close_1d_return`
Reason:
- first row in a series has no prior close
- prior close of zero also yields `None` in first-pass feature derivation

Not nullable:

- `ticker`
- `timeframe`
- `ts`
- `high_low_range`
- `close_open_delta`
- `feature_batch_id`
- `created_at`

## Identity And Uniqueness

Logical identity:

```text
(ticker, timeframe, ts)
```

First-pass unique constraint:

```text
UNIQUE (ticker, timeframe, ts)
```

Duplicate policy:

- duplicates are counted and skipped
- duplicates do not overwrite existing rows
- duplicates are not invalid feature rows

## Insert Column Order

Insert SQL must use this exact ordered column list:

- `ticker`
- `timeframe`
- `ts`
- `close_1d_return`
- `high_low_range`
- `close_open_delta`
- `feature_batch_id`

`created_at` remains DB-owned in first pass.

## Foreign Key Policy

First pass should include a foreign key to the canonical bar identity only if it can be done without schema distortion.

Recommended first-pass approach:

- no composite foreign key
- rely on shared `(ticker, timeframe, ts)` identity and feature selection from trusted `price_bars`

This keeps the schema lean for the first feature slice.

## First Test Expected Values

Using [`tests/fixtures/valid_daily.csv`](/Users/kogaryu/dev/pipbar/tests/fixtures/valid_daily.csv):

For `2024-01-02T00:00:00Z`

- `close_open_delta = -1.51`
- `high_low_range = 4.55`
- `close_1d_return = None`

For `2024-01-03T00:00:00Z`

- `close_open_delta = 0.03`
- `high_low_range = 2.45`
- `close_1d_return ~= -0.007488`

For `2024-01-04T00:00:00Z`

- `close_open_delta = -0.24`
- `high_low_range = 2.21`
- `close_1d_return ~= -0.012700`

For `2024-01-05T00:00:00Z`

- `close_open_delta = 2.63`
- `high_low_range = 3.43`
- `close_1d_return ~= 0.014898`

These values should be asserted in the first feature derivation test with an explicit float tolerance for returns.

## First-Pass Summary

This contract answers:

> "What exactly is a first-pass persisted feature row, and how should it behave on rerun?"
