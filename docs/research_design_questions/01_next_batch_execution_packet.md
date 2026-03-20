# Next Batch Execution Packet

This file exists to make the next research coding batch smooth.

It narrows the immediate target so the rest of the question pack does not become a generic ML-planning exercise.

## Recommended Next Slice

Build `app/research/` first.

Reason:

- it is the narrowest real consumer of the exported dataset layer
- it proves the full stack is usable for repeatable experiments
- it avoids premature ML framework sprawl
- it gives the repo a concrete research loop without inventing infrastructure

Do not start with:

- `app/ml/`
- `app/backtests/`
- `app/signals/`
- `app/experiments/`

## Exact First Vertical Slice

Target first-pass outcome:

- load exported dataset CSVs
- select the first-pass feature columns
- select `next_1d_return` as target
- run a zero-return regression baseline
- compute regression metrics on test rows
- return a stable research summary
- prove the slice with one end-to-end test
- ensure predictions align 1:1 with test rows
- verify metric inputs are equal length and ordered

## Files On Critical Path

Only these files are on the next critical path:

- `app/research/select.py`
- `app/research/baseline.py`
- `app/research/evaluate.py`
- `app/research/report.py`
- `app/research/research_runner.py`
- optional `app/models/research_result.py`
- one focused research test file
- `docs/research_contract.md`

Not on the immediate critical path:

- `app/ml/*`
- `app/backtests/*`
- `app/signals/*`
- experiment persistence tables
- model registries

## Recommended Build Order

1. lock research contract
2. optionally add `ResearchResult` model
3. implement `research/select.py`
4. verify row loading from exported dataset CSVs
4.1 verify column selection matches contract exactly
5. implement `research/baseline.py`
6. verify deterministic zero predictions
7. implement `research/evaluate.py`
8. pin expected metric values
9. implement `research/report.py`
10. implement `research/research_runner.py`
11. run one end-to-end research test

## Success Criteria

The next slice is successful only if all of these are true:

- train/validation/test CSVs load correctly
- the research layer selects the locked feature and target columns
- the baseline produces deterministic predictions
- metrics are computed correctly from test rows
- summary fields are stable and explicit
- one end-to-end test passes
- predictions length equals number of test rows
- metric calculations are manually verifiable for at least one row
- dataset row ordering is preserved from CSV

## Things To Defer

Do not add in the next batch:

- multiple baseline models
- sklearn dependency unless unavoidable
- model persistence
- research run tables
- hyperparameter systems
- notebook integration
- charting/report dashboards

## Hard Rules

- no code outside critical path files
- no abstraction beyond contract requirements
- no silent data coercion
- no skipping validation of assumptions
