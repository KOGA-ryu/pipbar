# Lock Order

This file defines which decisions must be locked before the next research coding batch starts.

The goal is not to answer everything.
The goal is to answer the minimum set of questions that prevents structure drift.

## Must Lock Before Any Research Code

- What exact dataset files are read?
- What exact feature columns are used?
- What exact target column is used?
- What exact baseline is used?
- What exact metrics are computed?
- What is the first end-to-end success test?
- ensure prediction alignment with test rows (1:1)
- ensure dataset row ordering is preserved from CSV

## Must Lock Before `research/select.py`

- CSV file names
- required columns
- missing-value policy
- output shape

## Must Lock Before `research/baseline.py`

- baseline name
- fit behavior
- predict behavior
- whether validation rows are used

## Must Lock Before `research/evaluate.py`

- metric formulas
- evaluation split
- empty-row behavior
- invalid-value behavior
- metric input alignment requirements (y_true vs y_pred length and order)

## Must Lock Before `research_runner.py`

- exact stage order
- required runner inputs
- summary shape
- failure conditions
- zero-row success behavior
- invariant checks for completed runs

## Can Defer Until After Research Slice Works

- linear regression baseline
- multiple baseline comparison
- persisted experiment tracking
- richer artifact export
- confidence intervals
- charts

## If A Decision Is Still Fuzzy

Use this fallback rule:

- choose the smallest explicit contract that supports one real research loop
- document the choice
- defer generalization until the slice is running and tested
- never expand scope to resolve ambiguity; constrain the problem instead
