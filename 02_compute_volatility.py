import pandas as pd
import numpy as np
from pathlib import Path

INPUT_DIR = Path("data/processed")
ROLL_WINDOW = 5

def compute_volatility(df):
    df = df.copy()
    df["log_ret"] = np.log(df["Close"] / df["Close"].shift(1))
    df["realized_vol"] = df["log_ret"].rolling(ROLL_WINDOW).std() * np.sqrt(252)
    return df

def load_ticker(ticker):
    path = INPUT_DIR / f"{ticker}.csv"
    df = pd.read_csv(path, header=[0,1], index_col=0, parse_dates=True)
    df.columns = df.columns.get_level_values(0)
    return df

for path in INPUT_DIR.glob("*.csv"):
    if "_vol" in path.stem:
        continue
    ticker = path.stem
    print(f"Processing {ticker}...")
    df = load_ticker(ticker)
    df = compute_volatility(df)
    df.to_csv(INPUT_DIR / f"{ticker}_vol.csv")
    print(f"Saved {ticker}_vol.csv")