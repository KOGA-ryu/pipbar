# Research Design Questions

This folder is a lock-before-build design packet for the next research-facing layer.

Purpose:

- define the minimum research layer that earns a real home in the repo
- ask only the questions needed to build the next honest slice
- keep `research/` narrow and consumer-facing
- prevent `ml/`, `experiments/`, and other junk-drawer folders from appearing early
- enforce deterministic, testable research contracts

Scope covered here:

- `app/research/`
- optional `app/models/research_result.py`
- first-pass baseline research loop (select -> baseline -> evaluate -> report)

How to use this packet:

1. Read `01_next_batch_execution_packet.md` first.
2. Use `02_lock_order.md` to decide what must be answered before code starts.
3. Answer `00_overview_questions.md` next.
4. Use the file-specific question docs only for files that belong to the immediate slice.
5. Lock contracts in docs before creating tables or code.
6. Build one vertical slice at a time.
7. Verify contracts with one real end-to-end test before expanding scope.

Core rule:

- `pipeline/` makes data trustworthy
- `features/` makes trusted data informative
- `labels/` defines target truth
- `datasets/` packages trustworthy inputs and targets for research
- `research/` consumes research-ready rows/files and produces baseline experiment results
- every prediction must align 1:1 with its corresponding dataset row

Files in this pack:

- `01_next_batch_execution_packet.md`
- `02_lock_order.md`
- `00_overview_questions.md`
- `research_select_questions.md`
- `research_baseline_questions.md`
- `research_evaluate_questions.md`
- `research_report_questions.md`
- `research_runner_questions.md`
- `models_research_result_questions.md`

Working rule for the next batch:

- do not answer every question before coding
- answer only the questions required to build the next real slice cleanly
- defer broader research-system questions until they reach the critical path
- do not optimize, generalize, or expand beyond the current vertical slice

## Hard Rules

- no code outside critical path files
- no abstraction beyond contract requirements
- no silent data coercion
- no skipping validation of assumptions
