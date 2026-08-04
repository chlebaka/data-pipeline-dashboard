"""Load Google Search Console CSV exports."""

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent.parent / "data"

COLUMN_NAMES = {
    "Dátum": "Date",
    "Kliknutia": "Clicks",
    "Zobrazenia": "Impressions",
    "MP": "CTR",
    "Pozícia": "Position",
    "Najlepšie dopyty": "Query",
}


def load_csv(filename: str) -> pd.DataFrame:
    """Read a single Search Console CSV export from the data directory."""
    path = DATA_DIR / filename
    return pd.read_csv(path, encoding="utf-8")

def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Translate Slovak Search Console headers to English column names."""
    return df.rename(columns=COLUMN_NAMES)

def parse_ctr(df: pd.DataFrame) -> pd.DataFrame:
    """Convert the CTR column from percentage strings to floats."""
    df = df.copy()
    df["CTR"] = df["CTR"].str.rstrip("%").astype(float) / 100
    return df

if __name__ == "__main__":
    df = parse_ctr(rename_columns(load_csv("Graf.csv")))
    print(df.head())
    print(f"\nRows: {len(df)}")
    print(f"CTR dtype: {df['CTR'].dtype}")