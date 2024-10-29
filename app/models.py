import sqlite3

def init_db():
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()

    # 로그 테이블 생성
    cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        level TEXT,
                        message TEXT
                    )''')
    conn.commit()
    conn.close()

