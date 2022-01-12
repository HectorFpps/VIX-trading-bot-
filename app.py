import yfinance as yf
import pandas as pd
import pandas_ta as ta
import streamlit as st
from datetime import datetime

#User input
chartPeriod = "600d"
interval = "1h"
rsiPeriod = 14
buyLimit = 50
sellLimit = 65
emaLength1 = 30
emaLength2 = 150
bbands1 = []
bbands2 = []
bollLength1 = None
bollLength2 = None
std1 = None
std2 = None
buys = []
sells = []


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

#def bband1(bbands1, df):
    #df = df.ta.bbands(length=bollLength1, std=std1)
    #df = df.values.tolist()
    
    #for i in range(len(df)):
        #bbands1 += [df[i][2]]
        
#def bband2(bbands2, df):
    #df = df.ta.bbands(length=bollLength2, std=std2)
    #df = df.values.tolist()
    
    #for i in range(len(df)):
        #bbands2 += [df[i][2]]


st.write("# Volatility Index Trading Bot")

rsiPeriod = int(st.text_input("-Input Desired Rsi Period"))
#buyLimit = int(st.text_input("-Input Desired Buy Limit"))
sellLimit = int(st.text_input("-Input Desired Sell Limit"))
emaLength1 = int(st.text_input("-Input Desired EMA1"))
emaLength2 = int(st.text_input("-Input Desired EMA2"))
#bollLength1 = int(st.text_input("-Input Desired Bollinger Length 1"))
#std1 = int(st.text_input("-Input Desired Standard 1"))
#bollLength2 = int(st.text_input("-Input Desired Bollinger Length 2"))
#std2 = int(st.text_input("-Input Desired Standard 2"))

price(prices, df)
RSI(rsi, df)
EMA1(ema1, df)
EMA2(ema2, df)
#bband1(bbands1, df)
#bband2(bbands2, df)


buyPrice = None
sellprice = None
inPosition = False
balance = 10000
balanceTrack = []

for i in range(len(prices)):

    if not inPosition:
        if float(prices[i]) < float(ema1[i]) and float(prices[i]) < float(ema2[i]) and float(prices[i] < buyLimit):
            buyPrice = prices[i]
            buys += [buyPrice]
            inPosition = True

    if inPosition:
        if rsi[i] > sellLimit:
            sellPrice = prices[i]
            sells += [sellPrice]
            inPosition = False
            balance = balance*sellPrice/buyPrice

    balanceTrack += [balance]

st.write("#### Price of VIX")
st.line_chart(prices)
st.write("#### Bot Balance")
st.line_chart(balanceTrack)

st.write(len(sells))
for i in rage(len(sells)):
    st.write("Buy Price: " + str(round(buys[i])) + ". Sell price: " + str(round(sell[i])) + " " + str(round(sell[i]/buy[i]),1) + str(datetime.now()))
