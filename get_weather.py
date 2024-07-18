import requests
import pandas as pd
from datetime import datetime, timedelta

# Visual Crossing Weather APIの設定
api_key = "WGPLJP357LBQE7KGMJ4MBG4GS"
base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
city = "tokyo"
unit_group = "metric"
content_type = "json"

# 現在の日付から10日前までの日付範囲を計算
end_date = datetime.now().date()
start_date = end_date - timedelta(days=10)

# APIリクエストURLの構築
weather_url = f"{base_url}{city}/{start_date}/{end_date}?unitGroup={unit_group}&key={api_key}&contentType={content_type}"

# 天気データの取得
weather_response = requests.get(weather_url)
weather_data = weather_response.json()

# 天気データをDataFrameに変換
weather_df = pd.DataFrame(weather_data['days'])
weather_df['City_id'] = city
weather_df = weather_df[['datetime', 'City_id', 'description', 'precip', 'temp']]
weather_df.columns = ['Timestamp', 'City_id', 'Weather_Description', 'Rain', 'Temp']

# 結果を表示
print(weather_df)