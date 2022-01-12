import yfinance as yf
import pandas as pd
import pandas_ta as ta
import streamlit as st

#User input
chartPeriod = "100d"
interval = "1h"
rsiPeriod = 14
buyLimit = 50
sellLimit = 65
emaLength1 = 30
emaLength2 = 150


#Market data
df = pd.DataFrame()
df = df.ta.ticker("^VIX", period=chartPeriod, interval=interval)
prices = []
rsi = []
ema1 = []
ema2 = []

def price(prices, df):

    df = df.values.tolist()
    for i in range(len(df)):
        prices += [df[i][3]]

def RSI(rsi, df):

    df = df.ta.rsi(length=rsiPeriod).to_frame()
    df = df.values.tolist()
    for i in range(len(df)):
        rsi += [df[i][0]]
        
def EMA1(ema1, df):
    df = df.ta.ema(length=emaLength1)
    df = df.values.tolist()
    
    for i in range(len(df)):
        ema1 += [df[i]]

def EMA2(ema2, df):
    df = df.ta.ema(length=emaLength2)
    df = df.values.tolist()
    
    for i in range(len(df)):
        ema2 += [df[i]]


st.write("# Volatility Index Trading Bot")

rsiPeriod = int(st.text_input("-Input Desired Rsi Period"))
buyLimit = int(st.text_input("-Input Desired Buy Limit"))
sellLimit = int(st.text_input("-Input Desired Sell Limit"))
emaLength1 = int(st.text_input("-Input Desired EMA1"))
emaLength2 = int(st.text_input("-Input Desired EMA2"))

price(prices, df)
RSI(rsi, df)
EMA1(ema1, df)
EMA2(ema2, df)


buyPrice = None
sellprice = None
inPosition = False
balance = 10000
balanceTrack = []

for i in range(len(prices)):

    if not inPosition:
        if float(prices[i]) < 19:
            buyPrice = prices[i]
            inPosition = True

    if inPosition:
        if float(rsi[i]) > sellLimit:
            sellPrice = prices[i]
            inPosition = False
            balance = balance*sellPrice/buyPrice

    balanceTrack += [balance]

st.write("#### Price of VIX")
st.line_chart(prices)
st.write("#### Bot Balance")
st.line_chart(balanceTrack)
