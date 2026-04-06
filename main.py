from fastapi import FastAPI

app = FastAPI()

# @ -> Python 데코레이터: 파이썬 함수에 추가적인 기능을 부여하는 문법
# GET / 요청이 들어오면, root_handler라는 함수를 실행하라
@app.get("/")
def root_handler():
    return {"ping": "pong"}

@app.get("/hello")
def hello_handler():
    return {"message": "Hello from FastAPI!"}

# 임시 데이터
users = [
        {"id": 1, "name": "alex", "job": "student"},
        {"id": 2, "name": "bob", "job": "sw engineer"},
        {"id": 3, "name": "chris", "job": "barista"},
    ]

# 전체 사용자 조회 API
@app.get("/users")
def get_users_handler():
    return users

# 주의!! 순서가 매우 중요(동적 변수보다 위에 있어야 실행됨)
@app.get("/users/search")
def search_user_handler():
    return ...

# 단일 사용자({}로 변수처리) 데이터 조회 API -> {user_id}번 사용자 데이터 조회
# path parameter
@app.get("/users/{user_id}")
def get_user_one_handler(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user
        # 없는 번호가 입력되면 None 반환



