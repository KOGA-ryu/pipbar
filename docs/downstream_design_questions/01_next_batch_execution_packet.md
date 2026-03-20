# Next Batch Execution Packet

This file exists to make the next coding batch smooth.

It narrows the immediate target so the rest of the question pack does not become an open-ended architecture seminar.

## Recommended Next Slice

Build `app/features/` first.

Reason:

- it is the closest downstream layer to trusted `price_bars`
- it keeps the next vertical slice deterministic
- it avoids tangling target definition with feature math
- it gives `labels/` and `datasets/` a stable upstream contract later

Do not start with `labels/` or `datasets/` first.

## Exact First Vertical Slice

Target first-pass outcome:

- select trusted bars from `price_bars`
- derive a tiny deterministic feature set
- validate feature rows
- load feature rows into `price_bar_features`
- print a summary
- prove the slice with one end-to-end test

First-pass feature set:

- `close_open_delta`
- `high_low_range`
- `close_1d_return`

- `close_open_delta = close - open`
- `high_low_range = high - low`
- `close_1d_return = (close_t / close_t-1) - 1`

First-pass identity:

- `(ticker, timeframe, ts)`

- rows are ordered by `ts` ascending before derivation

First-pass duplicate policy recommendation:

- duplicates are counted and skipped during load
- no overwrite or upsert behavior

- every selected row results in exactly one of: inserted / duplicate / rejected

Locked schema contract:

- see [`../feature_table_contract.md`](/Users/kogaryu/dev/pipbar/docs/feature_table_contract.md)

## Files On Critical Path

Only these files are on the next critical path:

- `app/models/price_bar_feature.py`
- `app/features/select.py`
- `app/features/derive.py`
- `app/features/validate.py`
- `app/features/load.py`
- `app/features/report.py`
- `app/features/feature_runner.py`
- DB schema additions needed for `price_bar_features`
- one focused feature test file

Not on the immediate critical path:

- `app/labels/*`
- `app/datasets/*`
- `app/models/label_row.py`
- `app/models/dataset_row.py`

Those files should stay design-only until the feature slice is real.

## Recommended Build Order

1. lock feature table contract
2. add `price_bar_features` schema
3. add `PriceBarFeature` model
4. implement `features/select.py`
5. implement `features/derive.py`
6. verify one derived row manually
6.1 verify first-row warmup behavior (`close_1d_return = None`)
7. implement `features/validate.py`
8. implement `features/load.py`
9. implement `features/report.py`
10. implement `features/feature_runner.py`
11. run one end-to-end test

## Success Criteria

The next slice is successful only if all of these are true:

- feature table initializes cleanly
- bars are selected deterministically
- feature rows derive with exact expected values
- invalid feature rows are handled explicitly
- valid feature rows insert into `price_bar_features`
- duplicate feature rows are counted and skipped
- summary counts are correct
- one end-to-end test passes

- first row per series has `close_1d_return = None`
- derived feature values match manually verified calculations
- row ordering is strictly time ascending before derivation

Pinned first-test values:

- `2024-01-02`: delta `-1.51`, range `4.55`, return `None`
- `2024-01-03`: delta `0.03`, range `2.45`, return approximately `-0.007488`
- `2024-01-04`: delta `-0.24`, range `2.21`, return approximately `-0.012700`
- `2024-01-05`: delta `2.63`, range `3.43`, return approximately `0.014898`

## Things To Defer

Do not add in the next batch:

- label tables
- dataset export logic
- ML code
- backtesting code
- broad feature libraries
- rolling-indicator sprawl
- feature run-tracking tables unless the slice proves it needs them
