from __future__ import annotations

from app.datasets.assemble import assemble_dataset_rows
from app.datasets.export import export_dataset_splits
from app.datasets.select import select_dataset_inputs
from app.datasets.split import split_dataset_rows


def run_dataset_build(
    db_path: str,
    output_path: str,
    ticker: str | None,
    timeframe: str,
    start_ts: str | None,
    end_ts: str | None,
    split_policy: str,
    selected_feature_columns: list[str] | None,
    selected_label_columns: list[str] | None,
    dataset_batch_id: str,
) -> dict[str, int | str]:
    if selected_feature_columns not in (None, ["close_1d_return", "high_low_range", "close_open_delta"]):
        raise ValueError("custom feature selection is not supported in first pass")
    if selected_label_columns not in (None, ["next_1d_return"]):
        raise ValueError("custom label selection is not supported in first pass")

    selected = select_dataset_inputs(
        db_path=db_path,
        ticker=ticker,
        timeframe=timeframe,
        start_ts=start_ts,
        end_ts=end_ts,
    )
    rows_selected = len(selected.bars)

    assembly_result = assemble_dataset_rows(
        bars=selected.bars,
        features=selected.features,
        labels=selected.labels,
    )
    rows_assembled = len(assembly_result.rows)

    splits = split_dataset_rows(assembly_result.rows, split_policy=split_policy)
    export_summary = export_dataset_splits(output_path=output_path, splits=splits)

    summary = {
        "rows_selected": rows_selected,
        "rows_assembled": rows_assembled,
        "rows_dropped_missing_features": assembly_result.rows_dropped_missing_features,
        "rows_dropped_missing_labels": assembly_result.rows_dropped_missing_labels,
        "rows_train": len(splits.train),
        "rows_validation": len(splits.validation),
        "rows_test": len(splits.test),
        "files_written": export_summary["files_written"],
        "output_path": output_path,
        "dataset_batch_id": dataset_batch_id,
    }
    _assert_dataset_summary_invariants(summary)
    print(summary)
    return summary


def _assert_dataset_summary_invariants(summary: dict[str, int | str]) -> None:
    total_split_rows = summary["rows_train"] + summary["rows_validation"] + summary["rows_test"]
    assert summary["rows_selected"] >= summary["rows_assembled"]
    assert summary["rows_dropped_missing_features"] >= 0
    assert summary["rows_dropped_missing_labels"] >= 0
    assert summary["rows_assembled"] == total_split_rows
    assert summary["files_written"] == 3
