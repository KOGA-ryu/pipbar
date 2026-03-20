# Research Overview Contract

## Purpose

This document defines the **first-pass research direction** for the pipbar system.

It converts open design questions into explicit, enforceable decisions that guide:

- research input selection
- baseline prediction
- metric evaluation
- research summary reporting

No research code should be written without alignment to this contract.

---

## First concrete outcome (locked)

The first research slice must answer:

```text
Given exported dataset CSVs, can we run one repeatable regression baseline and get stable metrics?
```

---

## Out of scope (first slice)

Explicitly NOT included:

- model registries
- experiment tracking systems
- hyperparameter tuning
- multiple baseline families
- classification targets
- backtesting
- signal generation
- notebooks

---

## Input contract (locked)

Research consumes **exported dataset CSV files only**:

- `train.csv`
- `validation.csv`
- `test.csv`

Rules:

- `test.csv` is required
- `train.csv` and `validation.csv` are optional
- empty splits are valid
- research does NOT read raw DB tables

---

## Dataset guarantees

Dataset rows must include:

- identifiers: `ticker`, `timeframe`, `ts`
- OHLCV values
- feature columns
- label column

Allowed blanks:

- warmup features (`close_1d_return` first row)
- tail labels (`next_1d_return` last row)

All other blanks are invalid.

---

## Feature and target selection (locked)

Feature columns:

- `close_1d_return`
- `high_low_range`
- `close_open_delta`

Target column:

- `next_1d_return`

Selection is fixed for first pass.

---

## Experiment policy (locked)

Baseline:

```text
predict 0.0 return for every row
```

Properties:

- no training phase
- deterministic
- stateless

Validation split:

- loaded but not required for metric calculation

Zero-row behavior:

- valid run
- metrics become `None`

---

## Metrics (locked)

Computed on **test split only**:

- `mae`
- `mse`
- `rmse`
- `directional_accuracy`

Rules:

- directional accuracy excludes rows where `y_true == 0`
- metric inputs must be equal length
- invalid values (`NaN`, `inf`) cause failure

---

## Output contract

Each research run returns:

- `dataset_batch_id`
- `target_column`
- `feature_columns`
- `baseline_name`
- `rows_train`
- `rows_validation`
- `rows_test`
- `mae`
- `mse`
- `rmse`
- `directional_accuracy`

Output type:

```text
ResearchResult
```

---

## Operational rules

- research runs must be deterministic
- malformed dataset files fail the run
- missing required columns fail the run
- first pass does not persist research runs in SQLite
- first pass does not train a model

---

## Build order (locked)

First research vertical slice must follow:

1. research contracts
2. optional `ResearchResult` model
3. `research/select.py`
4. `research/baseline.py`
5. `research/evaluate.py`
6. `research/report.py`
7. `research/research_runner.py`
8. one end-to-end research test
