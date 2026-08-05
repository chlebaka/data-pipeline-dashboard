"""Tests for the ingest module."""

import pandas as pd
import pytest

from src.ingest import load_csv, parse_ctr, rename_columns


def test_load_csv_returns_rows():
    df = load_csv("Graf.csv")
    assert len(df) > 0


def test_load_csv_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_csv("NoSuchFile.csv")


def test_rename_columns_translates_headers():
    df = pd.DataFrame({"Dátum": ["2025-08-02"], "Kliknutia": [5]})
    result = rename_columns(df)
    assert list(result.columns) == ["Date", "Clicks"]


def test_parse_ctr_converts_to_float():
    df = pd.DataFrame({"CTR": ["5.95%", "0%"]})
    result = parse_ctr(df)
    assert result["CTR"].tolist() == pytest.approx([0.0595, 0.0])


def test_parse_ctr_missing_column_raises():
    with pytest.raises(KeyError):
        parse_ctr(pd.DataFrame({"Clicks": [1]}))