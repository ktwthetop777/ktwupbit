import time
import pyupbit
import datetime

access = "SeOqwkvSjqERxW3Kmqc1tiZExaSGhMXbeK6k2lrr"
secret = "sJTM31h58x8hxH1pCsxRxdFix9A8n2cPEFcr4KPS"

def get_target_price(ticker, k):
    print("변동성 돌파 전략으로 매수 목표가 조회")
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    print("시작 시간 조회")
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    print("잔고 조회")
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    print("현재가 조회")
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
avg_price = 0
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-XRP")
        end_time = start_time + datetime.timedelta(days=1)
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-XRP", 0.4)
            current_price = get_current_price("KRW-XRP")
            if (avg_price *1.15 < current_price) and avg_price > 0:
                btc = get_balance("XRP")
                if btc > 0.00008:
                    upbit.sell_market_order("KRW-XRP", btc*0.9995)
                    avg_price = 0
            elif (avg_price * 0.9 > current_price) and avg_price > 0:
                btc = get_balance("XRP")
                if btc > 0.00008:
                    upbit.sell_market_order("KRW-XRP", btc*0.9995)
                    avg_price = 0
            if target_price < current_price and avg_price == 0:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-XRP", krw*0.9995)
                    avg_price = upbit.get_avg_buy_price("KRW-XRP")
        else:
            btc = get_balance("XRP")
            if btc > 0.00008:
                upbit.sell_market_order("KRW-XRP", btc*0.9995)
                avg_price = 0
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
