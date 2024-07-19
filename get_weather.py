import requests
import time
import pandas as pd
from datetime import datetime, timedelta

class GetWeather:
    def __init__(self, api_key, city='tokyo', unit_group = "metric", content_type = "json", range = 10):
        self.api_key = api_key
        self.city = city
        self.unit_group = unit_group
        self.content_type = content_type
        self.range = range
        self.base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"

        # 現在の日付からrangeまでの日付範囲を計算
        self.end_date = datetime.now().date()
        self.start_date = self.end_date - timedelta(days=range)

        # リトライ数とリトライ遅延
        self.max_retries = 5
        self.retry_delay = 5

    def fetch_data(self):
        for _ in range(self.max_retries):
            try:
                # APIにリクエストを送信
                url = f"{self.base_url}{self.city}/{self.start_date}/{self.end_date}?unitGroup={self.unit_group}&key={self.api_key}&contentType={self.content_type}"
                response = requests.get(url)
                response.raise_for_status()  # HTTPステータスコードが200以外の場合に例外を発生させる
                
                # レスポンスが正常な場合
                if response.status_code == 200:
                    data = response.json()
                    
                    # 各データを抽出
                    weather_df = pd.DataFrame(data['days'])
                    weather_df['City_id'] = self.city
                    weather_df = weather_df[['datetime', 'City_id', 'description', 'precip', 'temp']]
                    weather_df.columns = ['Timestamp', 'City_id', 'Weather_Description', 'Rain', 'Temp']
                    
                    return weather_df
                
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

if __name__ == "__main__":
    api_key = "WGPLJP357LBQE7KGMJ4MBG4GS"
    get_weather = GetWeather(api_key)
    print(get_weather.fetch_data())