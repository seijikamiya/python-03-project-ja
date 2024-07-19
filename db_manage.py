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
        df.to_sql(table_name, conn, index=False, if_exists='replace')

        # コミットして接続を閉じる
        conn.commit()
        conn.close()

def create_relationship(path):
        # SQLiteデータベースに接続
    conn = sqlite3.connect(path)

    # 主キーおよび外部キーの設定
    cursor = conn.cursor()

    # 主キーの設定
    cursor.execute('''
        CREATE TABLE stock_new (
            StockID INTEGER PRIMARY KEY,
            Date DATE,
            Open FLOAT,
            High FLOAT,
            Low FLOAT,
            Close FLOAT,
            Company_code TEXT,
            Diff FLOAT
        )
    ''')
    cursor.execute('INSERT INTO stock_new SELECT * FROM stock')
    cursor.execute('DROP TABLE stock')
    cursor.execute('ALTER TABLE stock_new RENAME TO stock')

    cursor.execute('''
        CREATE TABLE weather_new (
            WeatherID INTEGER PRIMARY KEY,
            Timestamp DATE,
            City_id TEXT,
            Weather_Description TEXT,
            Rain FLOAT,
            Temp FLOAT
        )
    ''')
    cursor.execute('INSERT INTO weather_new SELECT * FROM weather')
    cursor.execute('DROP TABLE weather')
    cursor.execute('ALTER TABLE weather_new RENAME TO weather')

    cursor.execute('''
        CREATE TABLE WeatherEffectNew (
            Weather_Description TEXT PRIMARY KEY,
            PriceDiff FLOAT,
            FOREIGN KEY(Weather_Description) REFERENCES weather(Weather_Description)
        )
    ''')
    cursor.execute('INSERT INTO WeatherEffectNew SELECT Weather_Description, PriceDiff FROM WeatherEffect')
    cursor.execute('DROP TABLE WeatherEffect')
    cursor.execute('ALTER TABLE WeatherEffectNew RENAME TO WeatherEffect')

    # 変更をコミットして接続を閉じる
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