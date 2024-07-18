import requests
import pandas as pd
import time

# Yahoo Finance APIのURL
url = 'https://query1.finance.yahoo.com/v8/finance/chart/9201.T'

# ヘッダーにUser-Agentを追加
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# パラメータを設定（直近10日分のデータ取得）
params = {
    'range': '10d',  # 直近10日分のデータ
    'interval': '1d'  # 日単位のデータ
}

# リトライ回数を設定
max_retries = 5
retry_delay = 5  # リトライする前に待機する秒数

for attempt in range(max_retries):
    # APIにリクエストを送信
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # 必要なデータを抽出
        timestamps = data['chart']['result'][0]['timestamp']
        indicators = data['chart']['result'][0]['indicators']['quote'][0]
        open_prices = indicators['open']
        high_prices = indicators['high']
        low_prices = indicators['low']
        close_prices = indicators['close']
        
        # タイムスタンプを日付に変換
        dates = pd.to_datetime(timestamps, unit='s').date
        
        # データをDataFrameに変換
        df = pd.DataFrame({
            'Date': dates,
            'Open': open_prices,
            'High': high_prices,
            'Low': low_prices,
            'Close': close_prices
        })
        
        # 日ごとにデータを集約
        df = df.groupby('Date').agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last'
        }).reset_index()
        
        # 直近10日分のデータを表示
        print(df)
        break  # 成功した場合、ループを抜ける
    elif response.status_code == 429:
        print(f"Rate limit exceeded. Retrying in {retry_delay} seconds...")
        time.sleep(retry_delay)  # 待機してから再試行
    else:
        print(f"Failed to fetch data: {response.status_code}")
        break  # 他のエラーの場合、ループを抜ける