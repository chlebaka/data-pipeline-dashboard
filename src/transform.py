"""Transform Search Console data into aggregated views."""

import pandas as pd


def aggregate_monthly(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate daily metrics into monthly totals and averages."""
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    monthly = df.groupby(df["Date"].dt.to_period("M")).agg(
        Clicks=("Clicks", "sum"),
        Impressions=("Impressions", "sum"),
        Position=("Position", "mean"),
    )
    monthly["CTR"] = monthly["Clicks"] / monthly["Impressions"]
    return monthly.reset_index()


if __name__ == "__main__":
    from ingest import load_csv, parse_ctr, rename_columns

    df = parse_ctr(rename_columns(load_csv("Graf.csv")))
    print(aggregate_monthly(df))