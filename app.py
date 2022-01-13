import yfinance as yf
import pandas as pd
import pandas_ta as ta
import streamlit as st
from datetime import datetime

# “1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”, “3mo”

#User input
chartPeriod = "600d"
interval = "1h"
rsiPeriod = 14
rsiBuy = 50
rsiSell = 65
ema1Buy = 30
ema2Buy = 150
ema1Sell = 30
ema2Sell = 150
bbands1 = []
bbands2 = []
bollLength1 = None
bollLength2 = None
std1 = None
std2 = None
buys = []
sells = []
ticker = "^VIX"

#conditions
useRsiBuy = False
useRsiSell = False
useEmaBuy = False
useEmaSell = False
useTwoEmaBuy = False
useTwoEmaSewll = False
useSellOverNumber1 = False
useSellOverNumber2 = False
useBuyUnderNumber1 = False
useBuyUnderNumber2 = False
sellOverNumber1 = 0
sellOverNumber2 = 0
buyUnderNumber1 = 0
buyUnderNumber2 = 0

#Market data
df = pd.DataFrame()
df = df.ta.ticker(ticker, period=chartPeriod, interval=interval)
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
        
        
#--------------------------------------------------------------------------------------------------------------------------------------------------


st.write("# Personal trading bot")

st.write("### What ticker do you want to trade: ")
ticker = st.text_input("Ticker of yahoo finance: ", value = "^VIX")

st.write("### Buy Condition")

useRsiBuy = st.checkbox('Use rsi for buy condition')
if(useRsiBuy):
    rsiBuy = st.number_input("Buy when rsi is under: ", value = 55, step = 1)
    
useEmaBuy = st.checkbox('Use ema for buy condition')
if(useEmaBuy):
    ema1Buy = st.number_input("Buy when over ema of what period: " , value = 10, step = 10)
    useBuyUnderNumber1 = st.checkbox("Buy under ema minus a number")
    if(useBuyUnderNumber1):
        buyUnderNumber1 = st.number_input("Buy under ema minus", value = 2, step = 1)
    useTwoEmaBuy = st.checkbox('Use two ema for buy condition')
    if(useTwoEmaBuy):
        useBuyUnderNumber2 = st.checkbox("Buy under ema minus a number")
        ema2Buy = st.number_input("Buy when under the " + str(ema1Buy) + " period ema and what second period: ", value = 200, step = 10)
        
if(useRsiBuy and useEmaBuy):
    st.warning("Please keep in mind it will only buy if both conditions are satidfide")


        
st.write("### Sell Condition")

useRsiSell = st.checkbox('Use rsi for sell condition')
if(useRsiSell):
    rsiSell = st.number_input("Sell when rsi is over: ", value = 60, step = 1)
    
useEmaSell = st.checkbox('Use ema for sell condition')
if(useEmaSell):
    ema1Sell = st.number_input("Sell when over ema of what period: ", value = 200, step = 10)
    useBuyUnderNumber2 = st.checkbox("Sell over ema plus a number")
    if(useBuyUnderNumber2):
        buyUnderNumber2 = st.number_input("Buy under ema minus", value = 2, step = 1)
    useTwoEmaSell = st.checkbox('Use two ema for sell condition')
    if(useTwoEmaSell):
        ema2Sell = st.number_input("Sell when under the " + str(ema1Sell) + " period ema and what second period: ", value = 400, step = 10)
       
if(useRsiSell and useEmaSell):
    st.warning("Please keep in mind it will only sell if both conditions are satisfide")

if(useRsiBuy or useRsiSell):
    st.write("### Necesari data")
    rsiPeriod = st.number_input("What is the desired rsi period for the buy and sell rsi", value = 14, step = 2)




#ema1 = int(st.text_input("-Input Desired EMA1"))
#ema2 = int(st.text_input("-Input Desired EMA2"))

#price(prices, df)
#RSI(rsi, df)
#EMA1(ema1, df)
#EMA2(ema2, df)
#bband1(bbands1, df)
#bband2(bbands2, df)


#buyPrice = None
#sellprice = None
#inPosition = False
#balance = 10000
#balanceTrack = []
#balanceTrackAfterSells = []

#for i in range(len(prices)):

#    if not inPosition:
#        if float(prices[i]) < float(ema1[i]) and float(prices[i]) < float(ema2[i]) and float(rsi[i] < buyLimit):
#            buyPrice = prices[i]
#            buys += [buyPrice]
#            inPosition = True

#    if inPosition:
#        if rsi[i] > sellLimit:
#            sellPrice = prices[i]
#            sells += [sellPrice]
#            inPosition = False
#            balance = balance*sellPrice/buyPrice
#            balanceTrackAfterSells += [balance]

#    balanceTrack += [balance]
#dayPercent = []

#for i in range(len(balanceTrack)-1):
#    dayPercent += [balanceTrack[i+1]/balanceTrack[i]*100-100]

#st.write("#### Price of VIX")
#st.line_chart(prices)
#st.write("#### Bot Balance")
#st.line_chart(balanceTrack)
#st.line_chart(dayPercent)

#for i in range(len(sells)):
#    st.write("Buy Price: " + str(round(buys[i])) + ". Sell price: " + str(round(sells[i])) + " (" + str(round(sells[i]/buys[i]*100-100,1)) + "%) Balance: " + str(round(balanceTrackAfterSells[i])))
