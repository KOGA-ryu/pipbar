from __future__ import annotations

from dataclasses import dataclass

from app.models.dataset_row import DatasetRow
from app.models.label_row import LabelRow
from app.models.price_bar import PriceBar
from app.models.price_bar_feature import PriceBarFeature


@dataclass
class DatasetAssemblyResult:
    rows: list[DatasetRow]
    rows_dropped_missing_features: int
    rows_dropped_missing_labels: int


def assemble_dataset_rows(
    bars: dict[tuple[str, str, str], PriceBar],
    features: dict[tuple[str, str, str], PriceBarFeature],
    labels: dict[tuple[str, str, str], LabelRow],
) -> DatasetAssemblyResult:
    rows: list[DatasetRow] = []
    rows_dropped_missing_features = 0
    rows_dropped_missing_labels = 0

    for key in sorted(bars.keys(), key=lambda value: value[2]):
        missing_feature = key not in features
        missing_label = key not in labels

        if missing_feature:
            rows_dropped_missing_features += 1
        if missing_label:
            rows_dropped_missing_labels += 1
        if missing_feature or missing_label:
            continue

        bar = bars[key]
        feature = features[key]
        label = labels[key]
        rows.append(
            DatasetRow(
                ticker=bar.ticker,
                timeframe=bar.timeframe,
                ts=bar.ts,
                open=bar.open,
                high=bar.high,
                low=bar.low,
                close=bar.close,
                volume=bar.volume,
                close_1d_return=feature.close_1d_return,
                high_low_range=feature.high_low_range,
                close_open_delta=feature.close_open_delta,
                next_1d_return=label.next_1d_return,
            )
        )

    return DatasetAssemblyResult(
        rows=rows,
        rows_dropped_missing_features=rows_dropped_missing_features,
        rows_dropped_missing_labels=rows_dropped_missing_labels,
    )
