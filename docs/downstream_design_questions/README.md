# Downstream Design Questions

This folder is a lock-before-build design packet for the next downstream territory.

Purpose:

- force file-by-file contract decisions before implementation
- keep folder additions tied to real responsibilities
- prevent downstream architecture drift from folklore or vibes
- give the next coding batch a narrow, explicit starting point
- enforce deterministic, testable downstream contracts

Scope covered here:

- `app/features/`
- `app/labels/`
- `app/datasets/`
- `app/models/price_bar_feature.py`
- `app/models/label_row.py`
- `app/models/dataset_row.py`

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
- every downstream row must have one clear fate (inserted / duplicate / rejected)

Files in this pack:

- `../feature_table_contract.md`
- `01_next_batch_execution_packet.md`
- `02_lock_order.md`
- `00_overview_questions.md`
- `features_select_questions.md`
- `features_derive_questions.md`
- `features_validate_questions.md`
- `features_load_questions.md`
- `features_report_questions.md`
- `features_feature_runner_questions.md`
- `labels_derive_questions.md`
- `labels_validate_questions.md`
- `labels_load_questions.md`
- `labels_label_runner_questions.md`
- `datasets_select_questions.md`
- `datasets_assemble_questions.md`
- `datasets_split_questions.md`
- `datasets_export_questions.md`
- `datasets_dataset_runner_questions.md`
- `models_price_bar_feature_questions.md`
- `models_label_row_questions.md`
- `models_dataset_row_questions.md`

Working rule for the next batch:

- do not answer every question before coding
- answer only the questions required to build the next real slice cleanly
- defer later-layer questions until their folder genuinely reaches the critical path
- do not optimize, generalize, or expand beyond the current vertical slice

Critical-path locked docs for the next feature batch:

- [`../feature_table_contract.md`](/Users/kogaryu/dev/pipbar/docs/feature_table_contract.md)
- [`01_next_batch_execution_packet.md`](/Users/kogaryu/dev/pipbar/docs/downstream_design_questions/01_next_batch_execution_packet.md)
- [`02_lock_order.md`](/Users/kogaryu/dev/pipbar/docs/downstream_design_questions/02_lock_order.md)
