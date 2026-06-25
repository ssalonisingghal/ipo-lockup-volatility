import pandas as pd
import yfinance as yf
from datetime import timedelta
from pathlib import Path

OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


universe = pd.read_csv("tickers.csv", parse_dates=["ipo_date", "lockup_date_est"])

BUFFER_DAYS = 110
EVENT_WINDOW = 60

def pull_ticker(ticker, lockup_date):
    start = (lockup_date - timedelta(days=BUFFER_DAYS)).strftime("%Y-%m-%d")
    end = (lockup_date + timedelta(days=BUFFER_DAYS)).strftime("%Y-%m-%d")
    data = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)
    if data.empty:
        print(f"No data returned for {ticker}")
        return None
    return data

for _, row in universe.iterrows():
    ticker = row["ticker"]
    lockup_date = row["lockup_date_est"]
    
    print(f"Pulling {ticker}...")
    data = pull_ticker(ticker, lockup_date)
    
    if data is None:
        continue
        
    data.to_csv(OUTPUT_DIR / f"{ticker}.csv")
    print(f"Saved {ticker}")