import yfinance as yf
import pandas as pd
import pandas_ta as ta
import streamlit as st
from datetime import datetime

# “1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”, “3mo”

#User input
chartPeriod = "5d"
interval = "1h"
rsiPeriod = 14
rsiBuy = 50
rsiSell = 65
ema1Buy = 30
ema2Buy = 150
ema1Sell = 30
ema2Sell = 150
buys = []
sells = []
ticker = "eth-usd"
testingRange = 30

#conditions
useRsiBuy = False
useRsiSell = False
useEmaBuy = False
useEmaSell = False
useTwoEmaBuy = False
useTwoEmaSewll = False
sellOverNumber1 = 0
sellOverNumber2 = 0
buyUnderNumber1 = 0
buyUnderNumber2 = 0

#Market data
prices = []
pricesInRange = []
rsi = []
ema1b = []
ema2b = []
ema1s = []
ema2s = []
balanceTrack = []
balanceAfterSells = []

############################
df = pd.DataFrame()
df = df.ta.ticker(ticker, period=chartPeriod, interval=interval)
st.write(df)
############################

