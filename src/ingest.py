"""Load Google Search Console CSV exports."""

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent.parent / "data"


def load_csv(filename: str) -> pd.DataFrame:
    """Read a single Search Console CSV export from the data directory."""
    path = DATA_DIR / filename
    return pd.read_csv(path, encoding="utf-8")

if __name__ == "__main__":
    df = load_csv("Graf.csv")
    print(df.head())
    print(f"\nRows: {len(df)}")