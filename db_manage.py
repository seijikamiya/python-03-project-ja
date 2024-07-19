from abc import ABC, abstractmethod
import sqlite3
from getyfin import GetYfin

class BaseDB(ABC):
    def __init__(self, path, table_name):
        self.path = path
        self.table_name = table_name

    @abstractmethod
    def create_db():
        pass

    # @abstractmethod
    # def insert_data():
    #     pass

class WeatherDB(BaseDB):
    pass

class StockDB(BaseDB):
    def create_db(self):
        ticker = '9201.T'  # 企業コード
        get_yfin = GetYfin(ticker)
        df = get_yfin.fetch_data()

        # SQLiteデータベースに接続（新しいデータベースを作成）
        conn = sqlite3.connect(self.path)

        # DataFrameをデータベースに書き込む
        df.to_sql(self.table_name, conn, index=False, if_exists='replace')

        # コミットして接続を閉じる
        conn.commit()
        conn.close()


def sql_query():
    # データベースファイルのパス
    db_path = "stock_weather.db"

    # SQLiteデータベースに接続
    conn = sqlite3.connect(db_path)

    # カーソルの作成
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weather")
    weather_data = cursor.fetchall()

    return weather_data

if __name__ == "__main__":
    stock_db = StockDB("example.db", "stock")
    stock_db.create_db()