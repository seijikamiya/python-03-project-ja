import requests
import pandas as pd
import time

class GetYfin:
    def __init__(self, ticker, range='10d', interval='1d'):
        self.ticker = ticker
        self.url = f'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}'
        
        # ユーザーエージェントがないと弾かれることがわかったので追加
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        # データ取得期間と取得インターバル
        self.params = {
            'range': range,
            'interval': interval
        }

        # リトライ数とリトライ遅延
        self.max_retries = 5
        self.retry_delay = 5

    def fetch_data(self):
        for _ in range(self.max_retries):
            try:
                # APIにリクエストを送信
                response = requests.get(self.url, headers=self.headers, params=self.params)
                response.raise_for_status()  # HTTPステータスコードが200以外の場合に例外を発生させる
                
                # レスポンスが正常な場合
                if response.status_code == 200:
                    data = response.json()
                    
                    # 各データを抽出
                    timestamps = data['chart']['result'][0]['timestamp']
                    indicators = data['chart']['result'][0]['indicators']['quote'][0]
                    open_prices = indicators['open']
                    high_prices = indicators['high']
                    low_prices = indicators['low']
                    close_prices = indicators['close']
                    
                    # タイムスタンプを日付に変換
                    dates = pd.to_datetime(timestamps, unit='s').date
                    
                    # DataFrameに変換
                    df = pd.DataFrame({
                        'Date': dates,
                        'Open': open_prices,
                        'High': high_prices,
                        'Low': low_prices,
                        'Close': close_prices
                    })
                    
                    # Company_codeをtickerから追加
                    df['Company_code'] = self.ticker
                    
                    return df
                
                elif response.status_code == 429:
                    # レート制限の場合
                    print(f"Rate limit exceeded. Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                
                else:
                    # その他のエラーの場合
                    print(f"Failed to fetch data: {response.status_code}")
                    return None

            except requests.exceptions.RequestException as e:
                # リクエストでエラーが出た場合
                print(f"An error occurred: {e}")
                return None
'''
# テスト用、データフレームを表示
ticker = '9201.T'  # 企業コード
get_yfin = GetYfin(ticker)
df = get_yfin.fetch_data()
if df is not None:
    print(df)
'''