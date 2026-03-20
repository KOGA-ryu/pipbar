CREATE TABLE IF NOT EXISTS import_runs (
    import_batch_id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    timeframe TEXT NOT NULL,
    input_path TEXT NOT NULL,
    status TEXT NOT NULL,
    started_at TEXT NOT NULL,
    completed_at TEXT,
    failure_reason TEXT,
    stage_failed TEXT,
    files_discovered INTEGER NOT NULL DEFAULT 0,
    rows_parsed INTEGER NOT NULL DEFAULT 0,
    rows_valid INTEGER NOT NULL DEFAULT 0,
    rows_invalid INTEGER NOT NULL DEFAULT 0,
    rows_inserted INTEGER NOT NULL DEFAULT 0,
    rows_duplicates_skipped INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS price_bars (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    timeframe TEXT NOT NULL,
    ts TEXT NOT NULL,
    open REAL NOT NULL,
    high REAL NOT NULL,
    low REAL NOT NULL,
    close REAL NOT NULL,
    volume INTEGER NOT NULL,
    source TEXT NOT NULL,
    import_batch_id TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    FOREIGN KEY (import_batch_id) REFERENCES import_runs(import_batch_id)
);

CREATE TABLE IF NOT EXISTS rejected_rows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    import_batch_id TEXT NOT NULL,
    ticker TEXT NOT NULL,
    file_path TEXT NOT NULL,
    raw_row_json TEXT NOT NULL,
    issues_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (import_batch_id) REFERENCES import_runs(import_batch_id)
);

CREATE TABLE IF NOT EXISTS price_bar_features (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    timeframe TEXT NOT NULL,
    ts TEXT NOT NULL,
    close_1d_return REAL,
    high_low_range REAL NOT NULL,
    close_open_delta REAL NOT NULL,
    feature_batch_id TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

CREATE TABLE IF NOT EXISTS price_bar_labels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    timeframe TEXT NOT NULL,
    ts TEXT NOT NULL,
    next_1d_return REAL,
    label_batch_id TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_price_bars_ticker_timeframe_ts
ON price_bars (ticker, timeframe, ts);

CREATE UNIQUE INDEX IF NOT EXISTS idx_price_bar_features_ticker_timeframe_ts
ON price_bar_features (ticker, timeframe, ts);

CREATE UNIQUE INDEX IF NOT EXISTS idx_price_bar_labels_ticker_timeframe_ts
ON price_bar_labels (ticker, timeframe, ts);
