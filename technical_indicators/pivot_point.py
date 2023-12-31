# Import dependencies
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import yfinance as yf
import datetime as dt
yf.pdr_override()

# input
symbol = "AMD"
market = "SPY"
start = dt.date.today() - dt.timedelta(days=365 * 2)
end = dt.date.today()

# Read data
dataset = yf.download(symbol, start, end)
benchmark = yf.download(market, start, end)

dataset["Returns"] = dataset["Adj Close"].pct_change().dropna()

# # Stock Pivot Points

# ## Standard Pivot Points
# Floor Pivot Points (Basic Pivot Points) - Support and Resistance
# https://www.investopedia.com/trading/using-pivot-points-for-predictions/
PP = pd.Series((dataset["High"] + dataset["Low"] + dataset["Close"]) / 3)
R1 = pd.Series(2 * PP - dataset["Low"])
S1 = pd.Series(2 * PP - dataset["High"])
R2 = pd.Series(PP + dataset["High"] - dataset["Low"])
S2 = pd.Series(PP - dataset["High"] + dataset["Low"])
R3 = pd.Series(dataset["High"] + 2 * (PP - dataset["Low"]))
S3 = pd.Series(dataset["Low"] - 2 * (dataset["High"] - PP))
R4 = pd.Series(dataset["High"] + 3 * (PP - dataset["Low"]))
S4 = pd.Series(dataset["Low"] - 3 * (dataset["High"] - PP))
R5 = pd.Series(dataset["High"] + 4 * (PP - dataset["Low"]))
S5 = pd.Series(dataset["Low"] - 4 * (dataset["High"] - PP))
P = pd.Series(
    (dataset["Open"] + (dataset["High"] + dataset["Low"] + dataset["Close"])) / 4
)  # Opening Price Formula
psr = {
    "P": P,
    "R1": R1,
    "S1": S1,
    "R2": R2,
    "S2": S2,
    "R3": R3,
    "S3": S3,
    "R4": R4,
    "S4": S4,
    "R5": R5,
    "S5": S5,
}
PSR = pd.DataFrame(psr)
dataset = dataset.join(PSR)
print(dataset.head())

# labels = ['Price','P','R1','S1','R2','S2','R3','S3']
pivot_point = pd.concat([dataset["Adj Close"], P, R1, S1, R2, S2, R3, S3], axis=1).plot(
    figsize=(18, 12), grid=True
)
plt.title("Stock Pivot Point")
plt.legend(["Price", "P", "R1", "S1", "R2", "S2", "R3", "S3"], loc=0)
plt.show()

dataset["Adj Close"]["2018-05-01":"2018-06-01"]
date_range = dataset[["Adj Close", "P", "R1", "S1", "R2", "S2", "R3", "S3"]][
    "2018-05-01":"2018-06-01"
]  # Pick Date Ranges

date_range.plot(figsize=(18, 12), grid=True)
plt.title("Stock Pivot Point")
plt.legend(["Price", "P", "R1", "S1", "R2", "S2", "R3", "S3"], loc=0)
plt.show()

ax = date_range.plot(figsize=(18, 12), grid=True)
ax.lines[0].set_linewidth(4)  # Plot Specific Line
plt.title("Stock Pivot Point")
plt.legend()
plt.show()

# ## Woodie's Pivot Points
# Woodie's Pivot Points
P = pd.Series((dataset["High"] + dataset["Low"] + 2 * dataset["Close"]) / 4)
R1 = pd.Series(2 * P - dataset["Low"])
S1 = pd.Series(2 * P - dataset["High"])
R2 = pd.Series(P + dataset["High"] - dataset["Low"])
S2 = pd.Series(P - dataset["High"] + dataset["Low"])
wpp = {"P": P, "R1": R1, "S1": S1, "R2": R2, "S2": S2}
WPP = pd.DataFrame(wpp)
# dataset = dataset.join(WPP)
print(WPP.head())

# ## Camarilla's Pivot Points
# Camarilla's Pivot Points
R1 = pd.Series((dataset["High"] - dataset["Low"]) * 1.1 / (2 + dataset["Close"]))
R2 = pd.Series((dataset["High"] - dataset["Low"]) * 1.1 / (4 + dataset["Close"]))
R3 = pd.Series((dataset["High"] - dataset["Low"]) * 1.1 / (6 + dataset["Close"]))
R4 = pd.Series((dataset["High"] - dataset["Low"]) * 1.1 / (12 + dataset["Close"]))
S1 = pd.Series((dataset["Close"] - (dataset["High"] - dataset["Low"]) * 1.1) / 12)
S2 = pd.Series((dataset["Close"] - (dataset["High"] - dataset["Low"]) * 1.1) / 6)
S3 = pd.Series((dataset["Close"] - (dataset["High"] - dataset["Low"]) * 1.1) / 4)
S4 = pd.Series((dataset["Close"] - (dataset["High"] - dataset["Low"]) * 1.1) / 2)
cpp = {"R1": R1, "S1": S1, "R2": R2, "S2": S2, "R3": R3, "S3": S3, "R4": R4, "S4": S4}
CPP = pd.DataFrame(cpp)
# dataset = dataset.join(CPP)
print(CPP.head())

# ## Tom DeMark's
# Tom DeMark's
dataset = yf.download(symbol, start, end)

h_l_c = dataset["Close"] < dataset["Open"]
h_lc = dataset["Close"] > dataset["Open"]
hl_c = dataset["Close"] == dataset["Open"]
P = np.zeros(len(dataset["Close"]))
P[h_l_c] = (
    dataset["High"][h_l_c] + 2.0 * dataset["Low"][h_l_c] + dataset["Close"][h_l_c]
)
P[h_lc] = 2.0 * dataset["High"][h_lc] + dataset["Low"][h_lc] + dataset["Close"][h_lc]
P[hl_c] = dataset["High"][hl_c] + dataset["Low"][hl_c] + 2.0 * dataset["Close"][hl_c]
S1 = P / 2.0 - dataset["High"]
R1 = P / 2.0 - dataset["Low"]
P = P / 4.0
tdm = {"P": P, "S1": S1, "R1": R1}
TDM = pd.DataFrame(tdm)
print(TDM.head())

# ## Fibonacci's Pivot Point
# Fibonacci's Pivot Points
PP = pd.Series((dataset["High"] + dataset["Low"] + dataset["Close"]) / 3)
R1 = pd.Series((PP + (dataset["High"] - dataset["Low"]) * 0.382))
R2 = pd.Series((PP + (dataset["High"] - dataset["Low"]) * 0.618))
R3 = pd.Series((PP + (dataset["High"] - dataset["Low"]) * 1.000))
S1 = pd.Series((PP - (dataset["High"] - dataset["Low"]) * 0.382))
S2 = pd.Series((PP - (dataset["High"] - dataset["Low"]) * 0.618))
S3 = pd.Series((PP - (dataset["High"] - dataset["Low"]) * 1.000))
fpp = {"PP": PP, "R1": R1, "S1": S1, "R2": R2, "S2": S2, "R3": R3, "S3": S3}
FPP = pd.DataFrame(fpp)
# dataset = dataset.join(CPP)
print(FPP.head())

# ## Chicago Floor Trading Pivotal Point
PP = pd.Series((dataset["High"] + dataset["Low"] + dataset["Close"]) / 3)
R1 = pd.Series(PP * 2 - dataset["Low"].shift())
R2 = pd.Series(PP + (dataset["High"].shift() - dataset["Low"].shift()))
S1 = pd.Series(PP * 2 - dataset["High"].shift())
S2 = pd.Series(PP - (dataset["High"].shift() - dataset["Low"].shift()))
CFpp = {"PP": PP, "R1": R1, "S1": S1, "R2": R2, "S2": S2}
CFPP = pd.DataFrame(CFpp)
print(CFPP.head())
