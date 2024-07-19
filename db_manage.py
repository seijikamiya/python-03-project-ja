from abc import ABC, abstractmethod
import sqlite3
import pandas as pd
from getyfin import GetYfin
from get_weather import GetWeather

class BaseDB(ABC):
    def __init__(self, path, table_name):
        self.path = path
        self.table_name = table_name

    @abstractmethod
    def create_db():
        pass

class WeatherDB(BaseDB):
    def create_db(self):
        get_weather = GetWeather()
        df = get_weather.fetch_data()
        df.index.name = 'WeatherID'

        # SQLiteデータベースに接続（新しいデータベースを作成）
        conn = sqlite3.connect(self.path)

        # DataFrameをデータベースに書き込む
        df.to_sql(self.table_name, conn, index=True, if_exists='replace')

        # コミットして接続を閉じる
        conn.commit()
        conn.close()

class StockDB(BaseDB):
    def create_db(self):
        ticker = '9201.T'  # 企業コード
        get_yfin = GetYfin(ticker)
        df = get_yfin.data_pipeline()
        df.index.name = 'StockID'

        # SQLiteデータベースに接続（新しいデータベースを作成）
        conn = sqlite3.connect(self.path)

        # DataFrameをデータベースに書き込む
        df.to_sql(self.table_name, conn, index=True, if_exists='replace')

        # コミットして接続を閉じる
        conn.commit()
        conn.close()


def sql_query(path, query):
    # データベースファイルのパス
    db_path = path

    # SQLiteデータベースに接続
    conn = sqlite3.connect(db_path)

    # カーソルの作成
    df = pd.read_sql_query(query, conn)

    return df

def df_to_sql(df, path, table_name):
        conn = sqlite3.connect(path)
        df.index.name = 'WeatherEffectID'
        df.to_sql(table_name, conn, index=True, if_exists='replace')

        # コミットして接続を閉じる
        conn.commit()
        conn.close()

if __name__ == "__main__":
    # stock_db = StockDB("stock_weather.db", "stock")
    # stock_db.create_db()
    # weather_db = WeatherDB("stock_weather.db", "weather")
    # weather_db.create_db()
    query = """
    SELECT weather_description, AVG(Diff) as PriceDiff FROM stock
    INNER JOIN weather
    ON stock.date == weather.Timestamp
    GROUP BY weather_description
    """
    df = sql_query("stock_weather.db", query)
    df_to_sql(df, "stock_weather.db", "WeatherEffect")
