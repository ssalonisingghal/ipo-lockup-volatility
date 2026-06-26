import pandas as pd
import numpy as np
import statsmodels.api as sm
from pathlib import Path

data = {
    "ticker": ["CRWV", "CRCL", "CHYM", "FIG", "KRMN", "HNGE"],
    "effect": [-0.19, -0.05, 0.05, 0.38, -0.10, -0.12],
    "first_day_pop": [0.0, 1.68, 0.37, 2.50, 0.36, 0.174],
    "ipo_proceeds_m": [1500, 1050, 864, 1200, 582, 437]
}

df = pd.DataFrame(data)
print(df)

X = df["first_day_pop"]
X = sm.add_constant(X)
y = df["effect"]

model = sm.OLS(y, X).fit()
print(model.summary())

