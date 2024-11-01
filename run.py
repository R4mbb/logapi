from app import create_app
from app.models import init_db

# 데이터베이스 초기화
init_db()

# 애플리케이션 실행
app = create_app()
if __name__ == "__main__":
    app.run(debug=True)

