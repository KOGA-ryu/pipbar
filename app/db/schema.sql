CREATE TABLE IF NOT EXISTS import_runs (
    import_batch_id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    timeframe TEXT NOT NULL,
    input_path TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL
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
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (import_batch_id) REFERENCES import_runs(import_batch_id)
);

CREATE TABLE IF NOT EXISTS rejected_rows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    import_batch_id TEXT NOT NULL,
    file_path TEXT NOT NULL,
    row_index INTEGER NOT NULL,
    raw_row_json TEXT NOT NULL,
    normalized_record_json TEXT,
    issues_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (import_batch_id) REFERENCES import_runs(import_batch_id)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_price_bars_ticker_timeframe_ts
ON price_bars (ticker, timeframe, ts);
