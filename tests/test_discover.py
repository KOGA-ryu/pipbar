from __future__ import annotations

from pathlib import Path

from app.pipeline.discover import discover_csv_files


def test_discover_csv_files_returns_only_csv_files_in_sorted_order(tmp_path: Path) -> None:
    (tmp_path / "zeta.csv").write_text("", encoding="utf-8")
    (tmp_path / "alpha.csv").write_text("", encoding="utf-8")
    (tmp_path / "middle.CSV").write_text("", encoding="utf-8")
    (tmp_path / "notes.txt").write_text("", encoding="utf-8")
    (tmp_path / "README").write_text("", encoding="utf-8")

    discovered_files = discover_csv_files(str(tmp_path))

    assert discovered_files == [
        str(tmp_path / "alpha.csv"),
        str(tmp_path / "middle.CSV"),
        str(tmp_path / "zeta.csv"),
    ]
    assert all(isinstance(path, str) for path in discovered_files)
