import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from config import Config

LOG_LEVELS = {"INFO": 1, "WARN": 2, "ERROR": 3}

# 로그 수집 함수
def log_message(level, message, source="default"):
    if level not in LOG_LEVELS:
        raise ValueError("Invalid log level")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(Config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO logs (timestamp, level, message, source)
        VALUES (?, ?, ?, ?)
    ''', (timestamp, level, message, source))
    conn.commit()
    conn.close()

# 오래된 로그 삭제
def delete_old_logs(days=30):
    conn = sqlite3.connect(Config.DB_PATH)
    cursor = conn.cursor()
    cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("DELETE FROM logs WHERE timestamp < ?", (cutoff_date,))
    conn.commit()
    conn.close()

# 로그 검색 필터링
def filter_logs(level=None, keyword=None, start_date=None, end_date=None):
    query = "SELECT * FROM logs WHERE 1=1"
    params = []
    if level:
        query += " AND level = ?"
        params.append(level)
    if keyword:
        query += " AND message LIKE ?"
        params.append(f"%{keyword}%")
    if start_date:
        query += " AND timestamp >= ?"
        params.append(start_date)
    if end_date:
        query += " AND timestamp <= ?"
        params.append(end_date)
    conn = sqlite3.connect(Config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

# 로그 빈도 및 오류 비율 분석
def analyze_log_frequency():
    conn = sqlite3.connect(Config.DB_PATH)
    df = pd.read_sql("SELECT timestamp, level FROM logs", conn)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    daily_counts = df.groupby(df["timestamp"].dt.date).size()
    conn.close()
    return daily_counts.to_dict()

def analyze_error_ratio():
    conn = sqlite3.connect(Config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM logs WHERE level='ERROR'")
    error_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM logs")
    total_count = cursor.fetchone()[0]
    conn.close()
    return {"error_ratio": error_count / total_count if total_count > 0 else 0}

