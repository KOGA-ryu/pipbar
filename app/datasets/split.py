from __future__ import annotations

from dataclasses import dataclass

from app.models.dataset_row import DatasetRow


@dataclass
class DatasetSplits:
    train: list[DatasetRow]
    validation: list[DatasetRow]
    test: list[DatasetRow]


def split_dataset_rows(rows: list[DatasetRow], split_policy: str) -> DatasetSplits:
    if split_policy != "time_70_15_15":
        raise ValueError(f"unsupported split_policy: {split_policy}")

    ordered_rows = sorted(rows, key=lambda row: row.ts)
    total_rows = len(ordered_rows)
    train_end = int(total_rows * 0.7)
    validation_end = train_end + int(total_rows * 0.15)

    return DatasetSplits(
        train=ordered_rows[:train_end],
        validation=ordered_rows[train_end:validation_end],
        test=ordered_rows[validation_end:],
    )
