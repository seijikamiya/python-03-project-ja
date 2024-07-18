import sqlite3

# データベースファイルのパス
db_path = "weather_stock.db"

# SQLiteデータベースに接続
conn = sqlite3.connect(db_path)

# カーソルの作成
cursor = conn.cursor()

try:
    # データベースへのクエリ例（天気データの挿入）
    cursor.execute("""
        INSERT INTO weather (date, city, temperature, precipitation, wind_speed)
        VALUES (?, ?, ?, ?, ?)
    """, ('2024-07-17', 'Tokyo', 28.5, 0.2, 3.5))

    # コミット（データベースへの変更を保存）
    conn.commit()

    # データベースへのクエリ例（株価データの挿入）
    cursor.execute("""
        INSERT INTO stock_prices (date, company, price)
        VALUES (?, ?, ?)
    """, ('2024-07-17', 'Apple', 150.25))

    # コミット（データベースへの変更を保存）
    conn.commit()

    # 全ての天気データを取得
    cursor.execute("SELECT * FROM weather")
    weather_data = cursor.fetchall()
    print("Weather data:")
    for data in weather_data:
        print(data)

    # 全ての株価データを取得
    cursor.execute("SELECT * FROM stock_prices")
    stock_data = cursor.fetchall()
    print("Stock prices:")
    for data in stock_data:
        print(data)

finally:
    # カーソルのクローズ
    cursor.close()

    # データベースの接続をクローズ
    conn.close()
