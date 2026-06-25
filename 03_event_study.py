import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

INPUT_DIR = Path("data/processed")
EVENT_WINDOW = 60

universe = pd.read_csv("tickers.csv", parse_dates=["ipo_date", "lockup_date_est"])

def make_event_time(ticker, lockup_date):
    path = INPUT_DIR / f"{ticker}_vol.csv"
    df = pd.read_csv(path, header=[0,1], index_col=0, parse_dates=True)
    df.columns = df.columns.get_level_values(0)
    df = df[["Close", "realized_vol"]].copy()
    df["realized_vol"] = pd.to_numeric(df["realized_vol"], errors="coerce")
    idx = df.index.get_indexer([lockup_date], method="nearest")[0]
    df["event_day"] = range(-idx, len(df) - idx)
    df = df[(df["event_day"] >= -EVENT_WINDOW) & (df["event_day"] <= EVENT_WINDOW)]
    return df

all_data = []

for _, row in universe.iterrows():
    ticker = row["ticker"]
    lockup_date = row["lockup_date_est"]
    df = make_event_time(ticker, lockup_date)
    df["ticker"] = ticker
    all_data.append(df)

combined = pd.concat(all_data)

avg_vol = combined.groupby("event_day")["realized_vol"].mean()

plt.figure(figsize=(10, 5))
plt.plot(avg_vol.index, avg_vol.values, color="#2F6F5E", linewidth=2)
plt.axvline(0, color="red", linestyle="--", linewidth=1, label="Lockup expiration")
plt.xlabel("Trading days relative to lockup date")
plt.ylabel("Average realized volatility (annualized)")
plt.title("Volatility around IPO lockup expiration")
plt.legend()
plt.tight_layout()
plt.savefig("lockup_volatility_chart.png", dpi=150)
plt.show()
print("Chart saved.")