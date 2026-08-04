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


def add_rolling_average(df: pd.DataFrame, window: int = 7) -> pd.DataFrame:
    """Add a rolling average of daily clicks to smooth out weekday noise."""
    df = df.copy()
    df["ClicksRolling"] = df["Clicks"].rolling(window=window).mean()
    return df


def add_month_over_month_change(df: pd.DataFrame) -> pd.DataFrame:
    """Add the percentage change in clicks compared to the previous month."""
    df = df.copy()
    df["ClicksChange"] = df["Clicks"].pct_change()
    return df


if __name__ == "__main__":
    from ingest import load_csv, parse_ctr, rename_columns

    daily = parse_ctr(rename_columns(load_csv("Graf.csv")))
    print(add_rolling_average(daily).tail())

    monthly = add_month_over_month_change(aggregate_monthly(daily))
    print(monthly)