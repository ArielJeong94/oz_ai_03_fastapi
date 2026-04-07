from fastapi import FastAPI, Path, Query
from request import UserCreateRequest
from response import UserResponse

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
# query parameter
@app.get("/users/search")
def search_user_handler(
    name: str | None = Query(None), 
    job: str | None = Query(None)
):
    # 둘 다 없을 때
    if name is None and job is None:
        return {"msg": "조회에 필요한 QueryParam이 필요합니다."}
    return {"name": name, "job": job}
    
    # 둘 다 보낼 때
    # for user in users:
    #     if name and job:
    #         if user["name"] == name and user["job"] == job:
    #             return user
    #         else:
    #             return None
    #     if user["name"] == name:
    #         return user
    #     if user["job"] == job:
    #         return user

# 단일 사용자({}로 변수처리) 데이터 조회 API -> {user_id}번 사용자 데이터 조회
# path parameter
@app.get("/users/{user_id}")
def get_user_one_handler(
    # user_id: int
    # ge: 이상(= Greater than or Equal to), le: 이하, max_digits=6: 최대 자릿수 6
    user_id: int = Path(..., ge=1),
):
    for user in users:
        if user["id"] == user_id:
            return user
        # 없는 번호가 입력되면 None 반환

# 회원 추가 API
# POST /users
@app.post("/users", response_model=UserResponse)
def create_user_handler(
    # 1) 사용자 데이터를 넘겨 받는다 + 유효성 검사
    body: UserCreateRequest
):
    # 2) 사용자 데이터를 저장한다
    new_user = {
        "id": len(users) + 1,
        "name": body.name,
        "job": body.job
    }
    users.append(new_user)
    # 3) 응답을 반환한다
    return new_user

