# Module Responsibilities

Each file should do one job.

## Stage Boundaries

- parse reads raw input only
- normalize converts raw values into canonical records
- validate accepts canonical records and returns pass/fail results
- load writes accepted records to storage
- report summarizes outcomes
- orchestration coordinates stage order and data flow

## Boundary Rules

- parse does not normalize
- normalize does not validate
- validate does not load
- load does not rediscover or reparse
- orchestration does not absorb stage internals

## Practical Standard

First-pass modules should stay small.

- one dataclass per model file when possible
- one or two public functions per stage file when possible
- extract helpers only after the vertical slice is working
