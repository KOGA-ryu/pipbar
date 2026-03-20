# Research Contract

This document locks the first-pass `app/research/` layer contract.

It exists so the next research code batch does not invent experiment semantics mid-build.

## Purpose

The research layer answers:

> "Given exported research-ready dataset files, can we run one simple repeatable experiment and get stable metrics?"

First pass is intentionally narrow.

## Input Files

First pass reads:

- `train.csv`
- `validation.csv`
- `test.csv`

All are expected in one dataset export directory.

## First-Pass Feature Columns

- `close_1d_return`
- `high_low_range`
- `close_open_delta`

## First-Pass Target Column

- `next_1d_return`

## First Baseline

Baseline name:

```text
zero_return_baseline
```

Prediction rule:

```text
predict 0.0 for every evaluation row
```

No fitting is required in first pass.

## First-Pass Metrics

Metrics:

- `mae`
- `mse`
- `rmse`
- `directional_accuracy`

Evaluation split:

- `test` only

## Directional Accuracy Definition

First-pass directional accuracy is:

```text
fraction of rows where sign(prediction) == sign(target)
```

Using:

- negative -> `-1`
- zero -> `0`
- positive -> `1`

Rows with `target = None` are not evaluated.

## Output Contract

Every research run must return at minimum:

- `dataset_batch_id`
- `baseline_name`
- `target_column`
- `feature_columns`
- `rows_train`
- `rows_validation`
- `rows_test`
- `mae`
- `mse`
- `rmse`
- `directional_accuracy`

## Operational Rules

- research runs must be deterministic
- malformed dataset files fail the run
- missing required columns fail the run
- first pass does not persist research runs in SQLite
- first pass does not train a model

## First End-to-End Test

The first test must prove:

- exported dataset files are loaded correctly
- first-pass feature columns and target column are selected correctly
- the zero baseline predicts deterministic values
- metrics are computed correctly on the test split
- the final summary is stable and explicit
