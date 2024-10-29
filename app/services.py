import pandas as pd
import sqlite3

DB_PATH = "logs.db"

# 데이터베이스에서 로그 조회
def get_logs():
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM logs"
    df = pd.read_sql(query, conn)
    conn.close()
    return df.to_dict(orient="records")

# 필터 조건을 받아 로그 필터링
def filter_logs(params):
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM logs WHERE "
    conditions = []

    # 필터 조건 추가 (예: 날짜, 키워드 등)
    if "date" in params:
        conditions.append(f"date = '{params['date']}'")
    if "level" in params:
        conditions.append(f"date = '{params['level']}'")

    query += " AND ".join(conditions) if conditions else "1"
    df = pd.read_sql(query, conn)
    conn.close()
    return df.to_dict(orient="records")
