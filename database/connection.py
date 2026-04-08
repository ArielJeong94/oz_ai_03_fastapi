# SQLAlchemy(웹서버에서만 이용? -> No. 다양한 케이스 커버 가능)를 이용해서 DB와 연결하는 코드
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 데이터베이스 접속
DATABASE_URL = "sqlite:///./local.db"    # /./local.db: 파일 형태로 현재 폴더에 만들어라

# Enginge: DB와 접속을 관리하는 객체
engine = create_engine(DATABASE_URL, echo=True)

# Session: 한 번의 DB 요청-응답 단위
SessionFactory = sessionmaker(
    bind=engine,
    # 데이터를 어떻게 다룰지를 조정하는 옵션
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)
