# ipo-lockup-volatility

## Overview
This project analyzes whether stock volatility changes around IPO lockup expirations(the date when insiders are first permitted to sell their shares) using daily price data from 6 companies that went public in 2025. Contrary to the supply-shock hypothesis, average volatility did not spike at day 0 but instead dipped around the lockup date and rose afterward, suggesting markets price in the expiration in advance.

## Methodology
[how you did it - bullet points, one per script]

## Methodology

- `01_pull_data.py` — pulls daily OHLCV price data from Yahoo Finance for each ticker, centered around the lockup expiration date
- `02_compute_volatility.py` — computes 5-day rolling annualized realized volatility from log returns for all 6 companies
- `03_event_study.py` — re-indexes each stock to event time (day 0 = lockup date) and plots average volatility from day -60 to +60
- `04_stats_test.py` — runs a one-sample t-test to determine whether post-lockup volatility is significantly higher than pre-lockup
- `05_regression.py` — runs an OLS regression to test whether first-day IPO pop predicts the magnitude of the lockup volatility effect

## Findings
- Average volatility showed no significant spike at lockup expiration (t-test p-value = 0.95), suggesting markets price in the event in advance
- First-day IPO pop is a statistically significant predictor of the lockup volatility effect (p = 0.042, R² = 0.685) — companies with more hype at IPO tend to see larger volatility increases after lockup
- Figma (250% first-day pop, effect = +0.38) and CoreWeave (0% pop, effect = -0.19) illustrate this pattern most clearly

## Limitations
- Sample size of 6 companies is too small to draw firm conclusions about the broader population of IPOs
- Lockup dates are estimated as IPO date + 180 days and have not been verified against each company's prospectus
- Figma is a significant outlier that may be driving the regression result

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Run scripts in order: `01_pull_data.py` → `02_compute_volatility.py` → `03_event_study.py` → `04_stats_test.py` → `05_regression.py`