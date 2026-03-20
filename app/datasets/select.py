from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

from app.db.connection import get_connection
from app.models.label_row import LabelRow
from app.models.price_bar import PriceBar
from app.models.price_bar_feature import PriceBarFeature

DatasetKey: TypeAlias = tuple[str, str, str]


@dataclass
class SelectedDatasetInputs:
    bars: dict[DatasetKey, PriceBar]
    features: dict[DatasetKey, PriceBarFeature]
    labels: dict[DatasetKey, LabelRow]


def select_dataset_inputs(
    db_path: str,
    ticker: str | None,
    timeframe: str,
    start_ts: str | None,
    end_ts: str | None,
) -> SelectedDatasetInputs:
    bar_query = """
    SELECT ticker, timeframe, ts, open, high, low, close, volume, source, import_batch_id
    FROM price_bars
    WHERE timeframe = ?
    """
    feature_query = """
    SELECT ticker, timeframe, ts, close_1d_return, high_low_range, close_open_delta, feature_batch_id
    FROM price_bar_features
    WHERE timeframe = ?
    """
    label_query = """
    SELECT ticker, timeframe, ts, next_1d_return, label_batch_id
    FROM price_bar_labels
    WHERE timeframe = ?
    """

    parameters: list[object] = [timeframe]
    if ticker is not None:
        bar_query += " AND ticker = ?"
        feature_query += " AND ticker = ?"
        label_query += " AND ticker = ?"
        parameters.append(ticker.upper())
    if start_ts is not None:
        bar_query += " AND ts >= ?"
        feature_query += " AND ts >= ?"
        label_query += " AND ts >= ?"
        parameters.append(start_ts)
    if end_ts is not None:
        bar_query += " AND ts <= ?"
        feature_query += " AND ts <= ?"
        label_query += " AND ts <= ?"
        parameters.append(end_ts)

    bar_query += " ORDER BY ts ASC"
    feature_query += " ORDER BY ts ASC"
    label_query += " ORDER BY ts ASC"

    with get_connection(db_path) as conn:
        bar_rows = conn.execute(bar_query, parameters).fetchall()
        feature_rows = conn.execute(feature_query, parameters).fetchall()
        label_rows = conn.execute(label_query, parameters).fetchall()

    bars: dict[DatasetKey, PriceBar] = {}
    for row in bar_rows:
        key = (row["ticker"], row["timeframe"], row["ts"])
        bars[key] = PriceBar(
            ticker=row["ticker"],
            timeframe=row["timeframe"],
            ts=row["ts"],
            open=row["open"],
            high=row["high"],
            low=row["low"],
            close=row["close"],
            volume=row["volume"],
            source=row["source"],
            import_batch_id=row["import_batch_id"],
        )

    features: dict[DatasetKey, PriceBarFeature] = {}
    for row in feature_rows:
        key = (row["ticker"], row["timeframe"], row["ts"])
        features[key] = PriceBarFeature(
            ticker=row["ticker"],
            timeframe=row["timeframe"],
            ts=row["ts"],
            close_1d_return=row["close_1d_return"],
            high_low_range=row["high_low_range"],
            close_open_delta=row["close_open_delta"],
            feature_batch_id=row["feature_batch_id"],
        )

    labels: dict[DatasetKey, LabelRow] = {}
    for row in label_rows:
        key = (row["ticker"], row["timeframe"], row["ts"])
        labels[key] = LabelRow(
            ticker=row["ticker"],
            timeframe=row["timeframe"],
            ts=row["ts"],
            next_1d_return=row["next_1d_return"],
            label_batch_id=row["label_batch_id"],
        )

    return SelectedDatasetInputs(
        bars=bars,
        features=features,
        labels=labels,
    )
