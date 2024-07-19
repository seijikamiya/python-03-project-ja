from db_manage import StockDB, WeatherDB, sql_query, df_to_sql

def main():
    #APIで株の情報を取得
    stock_db = StockDB("stock_weather.db", "stock")
    stock_db.create_db()

    #APIで天気の情報を取得
    weather_db = WeatherDB("stock_weather.db", "weather")
    weather_db.create_db()

    #株と天気のテーブルをつなげて新しいテーブルを作成
    query = """
            SELECT weather_description, AVG(Diff) as PriceDiff FROM stock
            INNER JOIN weather
            ON stock.date == weather.Timestamp
            GROUP BY weather_description
            """

    df = sql_query("stock_weather.db", query)
    df_to_sql(df, "stock_weather.db", "WeatherEffect")

if __name__ == "__main__":
    main()