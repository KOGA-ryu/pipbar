# Phase Build Method

This repo uses a phased build method to keep implementation honest.

## Phase 0

Phase 0 is structure only.

- create folders
- create file placeholders
- write core docs
- do not start implementing behavior

## Phase 1

Phase 1 is the first vertical slice.

- pick one known input format
- implement only the minimum path needed to run end to end
- keep assumptions explicit and narrow
- prefer real code over abstraction

## Build Order

Lock build order before implementation starts.

- schema first
- connection and DB init next
- canonical model next
- pipeline stages in dependency order
- orchestration after stage modules
- entrypoint after orchestration
- one end-to-end test before expansion

## Verification Rhythm

Verify after each step or each tightly related pair of steps.

- do not continue if the current foundation is broken
- inspect real intermediate artifacts
- prefer one real check over a theoretical argument

## Anti-Drift Rule

Do not add work from later phases during the current phase.

- no feature drift
- no premature optimization
- no abstraction for work that does not exist yet
