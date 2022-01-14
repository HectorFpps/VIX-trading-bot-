import yfinance as yf
import pandas as pd
import pandas_ta as ta
import streamlit as st

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
ticker = "^VIX"
testingRange = 30
startingBalance = 10000
liquidated = False

#conditions
useRsiBuy = False
useRsiSell = False
useEmaBuy = False
useEmaSell = False
useTwoEmaBuy = False
useTwoEmaSell = False
sellOverNumber1 = 0
sellOverNumber2 = 0
buyUnderNumber1 = 0
buyUnderNumber2 = 0
leverage = 1


#Market data
prices = []
pricesInRange = []
ema1bInRange = []
ema2bInRange = []
ema1sInRange = []
ema2sInRange = []
rsi = []
ema1b = []
ema2b = []
ema1s = []
ema2s = []
balanceTrack = []
balanceAfterSells = []
pandl = []
dates = []
datesBuys = []

############################
df = pd.DataFrame()
############################

def price(prices, df):
    global dates
    df = df.values.tolist()
    for i in range(len(df)):
        prices += [df[i][3]]
        
def RSI(rsi, df):
    df = df.ta.rsi(length=rsiPeriod).to_frame()
    df = df.values.tolist()
    for i in range(len(df)):
        rsi += [df[i][0]]
        
def EMA1B(ema1b, df):
    global buyUnderNumber1
    df = df.ta.ema(length=ema1Buy)
    df = df.values.tolist()
    
    for i in range(len(df)):
        ema1b += [df[i]-buyUnderNumber1]

def EMA2B(ema2b, df):
    global buyUnderNumber2
    df = df.ta.ema(length=ema2Buy)
    df = df.values.tolist()
    
    for i in range(len(df)):
        ema2b += [df[i]-buyUnderNumber2]
        
def EMA1S(ema1s, df):
    global sellOverNumber1
    df = df.ta.ema(length=ema1Sell)
    df = df.values.tolist()
    
    for i in range(len(df)):
        ema1s += [df[i]+sellOverNumber1]

def EMA2S(ema2s, df):
    global sellOverNumber2
    df = df.ta.ema(length=ema2Sell)
    df = df.values.tolist()
    
    for i in range(len(df)):
        ema2s += [df[i]+sellOverNumber]
        
        
def calculate():
    global rsiBuy
    global rsiSell
    global useRsiBuy
    global useRsiSell
    global prices
    global ema1b
    global ema2b
    global ema1s
    global ema2s
    
    
    if not useRsiBuy:
        rsiBuy = 100
    if not useRsiSell:
        rsiSell = 0
    price(prices, df)
    RSI(rsi, df)
    
    
    if useEmaBuy:
        EMA1B(ema1b, df)
        if useTwoEmaBuy:
            EMA2B(ema2b, df)
        else:
            for i in range(len(prices)):
                ema2b += [1000000]
                
    else:
        for i in range(len(prices)):
            ema1b += [1000000]
            ema2b += [1000000]
            
    if useEmaSell:
        EMA1S(ema1s, df)
        if useTwoEmaSell:
            EMA2S(ema2s, df)
        else:
            for i in range(len(prices)):
                ema2s += [0]
    else:
        for i in range(len(prices)):
            ema1s += [0]
            ema2s += [0]
    
    
def trade():
    global rsiBuy
    global rsiSell
    global ema1b
    global ema2b
    global ema1s
    global ema2s
    global prices
    global buys
    global sells
    global buyUnderNumber1
    global buyUnderNumber2
    global sellUnderNumber1
    global sellUnderNumber2
    global balanceTrack
    global balanceAfterSells
    global pricesInRange
    global testingRange
    global startingBalance
    global pandl
    global dates
    global datesBuys
    global ema1bInRange
    global ema1sInRange
    global ema2bInRange
    global ema2sInRange
    
    calculate()
    
    buyPrice = None
    sellprice = None
    inPosition = False
    balance = startingBalance
    now = None
    
    for i in range(len(prices)-testingRange,len(prices)):
    #for i in range(len(prices)):
        pricesInRange += [prices[i]]
        ema1bInRange += [ema1b[i]]
        ema2bInRange += [ema2b[i]]
        ema1sInRange += [ema1s[i]]
        ema2sInRange += [ema2s[i]]
        if not inPosition:
            now = balance
            if rsi[i] < rsiBuy and prices[i] < ema1b[i] and prices[i] < ema2b[i]:
                buyPrice = prices[i]
                buys += [buyPrice]
                inPosition = True
                        
                
        if inPosition:
            now = balance+(balance * (prices[i]-buyPrice)/buyPrice*leverage)
            if rsi[i] > rsiSell and prices[i] > ema1s[i] and prices[i] > ema2s[i]:
                sellPrice = prices[i]
                sells += [sellPrice]
                inPosition = False
                balance += balance * (sellPrice-buyPrice)/buyPrice*leverage
                datesBuys += [dates[i]]
                balanceAfterSells += [balance]
        
        if now <= 0:
            balance = 0
            
        pandl += [now] 
        
        balanceTrack += [balance]
    
#--------------------------------------------------------------------------------------------------------------------------------------------------


st.write("# Personal trading bot")

st.write("### What ticker do you want to trade: ")
ticker = st.text_input("Ticker of yahoo finance: ", value = "^VIX")

interval = st.selectbox(
     'What candlestick inverval?',
     ('1m', '2m', '5m','15m','30m','60m','90m','1h','1d','5d'),index=7)

chartPeriod = st.selectbox(
     'How many data shoud it download?',
     ('1h','2h','12h','1d','2d', '5d','15d','30d','60d','100d','200d','300d','400d','600d','800d'),index = 13)

testingRange = st.slider("How many days shoud the strategy test?", min_value = 2, max_value = 800)

multi = int(interval[:-1])

if "m" in interval:
    testingRange *= (7*60*multi)
else:
    testingRange *= multi*7

st.write("### Buy Condition")

useRsiBuy = st.checkbox('Use rsi for buy condition')
if(useRsiBuy):
    rsiBuy = st.number_input("Buy when rsi is under: ", value = 55, step = 1)
    
useEmaBuy = st.checkbox('Use ema for buy condition')
if(useEmaBuy):
    ema1Buy = st.number_input("Buy when over ema of what period: " , value = 10, step = 10)
    buyUnderNumber1 = st.number_input("Buy under ema minus: ", value = 0, step = 1)
    useTwoEmaBuy = st.checkbox('Use two ema for buy condition')
    if(useTwoEmaBuy):
        ema2Buy = st.number_input("Buy when under the " + str(ema1Buy) + " period ema and what second period: ", value = 200, step = 10)
        buyUnderNumber2 = st.number_input("Buy under ema2 minus: ", value = 0, step = 1)
        
if(useRsiBuy and useEmaBuy):
    st.warning("Please keep in mind it will only buy if both conditions are satidfide")


        
st.write("### Sell Condition")

useRsiSell = st.checkbox('Use rsi for sell condition')
if(useRsiSell):
    rsiSell = st.number_input("Sell when rsi is over: ", value = 60, step = 1)
    
useEmaSell = st.checkbox('Use ema for sell condition')
if(useEmaSell):
    ema1Sell = st.number_input("Sell when over ema of what period: ", value = 200, step = 10)
    sellOverNumber1 = st.number_input("Sell over ema plus: ", value = 0, step = 1)
    useTwoEmaSell = st.checkbox('Use two ema for sell condition')
    if(useTwoEmaSell):
        ema2Sell = st.number_input("Sell when under the " + str(ema1Sell) + " period ema and what second period: ", value = 400, step = 10)
        sellOverNumber2 = st.number_input("Sell over ema2 plus: ", value = 0, step = 1)
       
if(useRsiSell and useEmaSell):
    st.warning("Please keep in mind it will only sell if both conditions are satisfide")

st.write("### Necesari data")    
leverage = st.slider("How much leveradge for your trades?", min_value = 1, max_value = 10)
startingBalance = st.number_input("Starting balance: ", value = 10000, step = 10000)
if(useRsiBuy or useRsiSell):
    rsiPeriod = st.number_input("What is the desired rsi period for the buy and sell rsi", value = 14, step = 2)

df = df.ta.ticker(ticker, period=chartPeriod, interval=interval)
for i in range(len(df)):
    dates += [df.index[i]]
    
st.markdown(f'<p style="background-color:#0066cc;color:#33ff33;font-size:24px;border-radius:2%;">"Hello"</p>', unsafe_allow_html=True)

calculateButton = st.button("Calculate")

if(calculateButton):
    trade()
    
    if not useEmaBuy:
        for i in range(len(ema1bInRange)):
            ema1bInRange[i] = 0
        for i in range(len(ema2bInRange)):
            ema2bInRange[i] = 0
         
    if not useEmaSell:
        for i in range(len(ema1sInRange)):
            ema1sInRange[i] = 0
        for i in range(len(ema2sInRange)):
            ema2sInRange[i] = 0
         
    if not useTwoEmaBuy:
        for i in range(len(ema2bInRange)):
            ema2bInRange[i] = 0
            
    if not useTwoEmaSell:
        for i in range(len(ema2sInRange)):
            ema2sInRange[i] = 0
            
            
    #resultDataframe = pd.DataFrame(list(zip(prices, rsi, ema1b, ema2b, ema1s, ema2s)),
    #           columns =['Price', 'Rsi' , 'Buy ema 1', 'Buy ema 2', 'Sell ema 1', 'Sell ema 2'])
    
    chartDataframe = pd.DataFrame(list(zip(pricesInRange, ema1bInRange, ema2bInRange, ema1sInRange, ema2sInRange)),
               columns =['Price', 'Buy ema 1', 'Buy ema 2', 'Sell ema 1', 'Sell ema 2'])
    
    #st.line_chart(pricesInRange)
    st.line_chart(chartDataframe)
    st.line_chart(pandl)
    st.line_chart(balanceTrack)
    
    
    st.write("###### Making trades from: "+ str(dates[len(prices)-testingRange]) + " to " + str(dates[len(prices)-1]))
    st.write("#### Starting balance: " + str(round(startingBalance)) + "$.")
    st.write("#### End balance: " + str(round(balanceTrack[-1])) + "$.")
    st.write("#### Profit: " + str(round(balanceTrack[-1]-startingBalance)) + "$.")
    st.write("#### Profit(%): " + str(round((balanceTrack[-1]-startingBalance)/startingBalance*100,1)) + "%.")
    st.write("#### Change: "+ str(round(balanceTrack[-1]/startingBalance,1)) + "x")
    
    
    for i in range(len(balanceAfterSells)):
        st.write("Date: " + str(datesBuys[i]) + " Trade number " + str(i+1) + ": Buy: " + str(round(buys[i],1)) + "$ Sell: " + str(round(sells[i],1)) + "$ Profit/Loss: " + str(round(balanceTrack[i] * ((sells[i]-buys[i])/buys[i]*leverage),1)) + "$ Percentage: " + str(round((sells[i]-buys[i])/buys[i]*100*leverage,1)) + "% Balance: " + str(round(balanceAfterSells[i])) + "$.")
        
    
    


