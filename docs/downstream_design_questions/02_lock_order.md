# Lock Order

This file defines which decisions must be locked before the next coding batch starts.

The goal is not to answer everything.
The goal is to answer the minimum set of questions that prevents structure drift.

## Must Lock Before Any Feature Code

- What is the exact `price_bar_features` row identity?
- What are the exact first-pass feature columns?
- What is the exact formula for each first-pass feature?
- What is the duplicate policy for feature rows?
- What counts must the feature summary include?
- What is the first end-to-end success test?
- What is the expected behavior for first-row warmup (e.g. close_1d_return = None)?
- Are selected bars guaranteed to be ordered by ts before derivation?
- What is the row fate rule for feature rows (inserted / duplicate / rejected)?

## Must Lock Before Feature Load Code

- Table name
- ordered insert columns
- uniqueness constraint
- duplicate skip policy
- whether transaction ownership stays in runner

## Must Lock Before Feature Runner Code

- exact stage order
- required runner inputs
- expected summary shape
- invariant checks for completed runs
- what qualifies as a successful zero-row run
- what conditions must fail the run vs be counted as invalid rows

## Can Defer Until After Feature Slice Works

- feature rejection persistence
- feature-specific run tables
- label schema
- dataset schema
- export formats beyond CSV
- train/validation/test split policy details

## If A Decision Is Still Fuzzy

Use this fallback rule:

- choose the smallest explicit contract that supports one real vertical slice
- document the choice
- defer generalization until the slice is running and tested
- never expand scope to solve uncertainty; constrain instead
