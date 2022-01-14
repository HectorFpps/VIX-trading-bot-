import yfinance as yf
import pandas as pd
import pandas_ta as ta
import streamlit as st
from datetime import datetime

# “1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”, “3mo”

#User input
chartPeriod = "5d"
interval = "1h"
ticker = "eth-usd"

df = pd.DataFrame()
df = df.ta.ticker(ticker, period=chartPeriod, interval=interval)
st.write(df)
