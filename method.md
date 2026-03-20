# Method

This project is organized to prove one working ingestion slice before the system expands.

## Why It Works

The method is simple:

- define contracts first
- lock phase boundaries
- assign one job per module
- build in dependency order
- verify with real checks as you go

## Operating Law

Every feature slice must satisfy two gates before it moves on:

- contract lock before implementation
- claim-matched proof before completion

Contract lock means the slice starts with:

- the data shape
- the function return shape
- the verification statement

Claim-matched proof means the verification must demonstrate the exact behavior being claimed. If the claim is rerun safety, the proof must show a real rerun. If the claim is duplicate handling, the proof must show real duplicates.

This keeps the repo understandable while requirements are still moving.

## Reusable Parts

These parts are intended to carry into future repos:

- phased build method
- contracts-first planning
- strict stage boundaries
- small-batch review rhythm
- profile-before-optimization policy
- starter checklist

## Project-Specific Parts

These parts belong to pipbar, not to the method itself:

- the market-data schema
- the CSV fixture format
- the exact pipeline stage names
- the SQLite implementation details

## Standard

The goal is not to preserve a vibe. The goal is to preserve a repeatable decision structure.

See [`docs/project_standards/phase_build_method.md`](/Users/kogaryu/dev/pipbar/docs/project_standards/phase_build_method.md),
[`docs/project_standards/module_responsibilities.md`](/Users/kogaryu/dev/pipbar/docs/project_standards/module_responsibilities.md),
[`docs/project_standards/contracts_first.md`](/Users/kogaryu/dev/pipbar/docs/project_standards/contracts_first.md),
[`docs/project_standards/review_rhythm.md`](/Users/kogaryu/dev/pipbar/docs/project_standards/review_rhythm.md),
and [`docs/project_standards/future_optimization_policy.md`](/Users/kogaryu/dev/pipbar/docs/project_standards/future_optimization_policy.md).
