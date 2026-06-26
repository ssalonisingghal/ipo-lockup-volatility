import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path

INPUT_DIR = Path("data/processed")
EVENT_WINDOW = 60

universe = pd.read_csv("tickers.csv", parse_dates=["ipo_date", "lockup_date_est"])

def compute_effect(ticker, lockup_date):
    path = INPUT_DIR / f"{ticker}_vol.csv"
    df = pd.read_csv(path, header=[0,1], index_col=0, parse_dates=True)
    df.columns = df.columns.get_level_values(0)
    df["realized_vol"] = pd.to_numeric(df["realized_vol"], errors="coerce")
    
    idx = df.index.get_indexer([lockup_date], method="nearest")[0]
    df["event_day"] = range(-idx, len(df) - idx)
    
    pre = df[(df["event_day"] >= -EVENT_WINDOW) & (df["event_day"] < 0)]["realized_vol"].mean()
    post = df[(df["event_day"] > 0) & (df["event_day"] <= EVENT_WINDOW)]["realized_vol"].mean()
    
    return post - pre

effects = []

for _, row in universe.iterrows():
    ticker = row["ticker"]
    lockup_date = row["lockup_date_est"]
    effect = compute_effect(ticker, lockup_date)
    print(f"{ticker}: {effect:.4f}")
    effects.append(effect)

effects = np.array(effects)

t_stat, p_value = stats.ttest_1samp(effects, popmean=0)
print(f"\nMean effect: {effects.mean():.4f}")
print(f"T-statistic: {t_stat:.4f}")
print(f"P-value: {p_value:.4f}")