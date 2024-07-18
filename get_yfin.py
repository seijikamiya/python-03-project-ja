#yfinanceモジュールを利用して動作することを確認

import yfinance as yf
import pandas as pd
import datetime
import pytz

def get_highs_last_10_days(ticker):
    # 今日の日付を取得
    today = datetime.datetime.now(pytz.timezone('Asia/Tokyo')).date()
    
    # 10日前の日付を取得
    start_date = today - datetime.timedelta(days=10)
    
    # 銘柄のデータを取得
    stock = yf.Ticker(ticker)
    hist = stock.history(start=start_date, end=today + datetime.timedelta(days=1))
    
    # 日付を日本時間に変換
    hist.index = hist.index.tz_convert('Asia/Tokyo')
    
    # 過去10日間の最高値のみを取得
    highs = hist[['High']].tail(10)
    
    return highs

# 例: 日本航空の過去10日間の最高値を取得
ticker = "9201.T"
highs = get_highs_last_10_days(ticker)
print(highs)