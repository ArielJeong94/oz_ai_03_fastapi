from fastapi import APIRouter, Path, Query, status, HTTPException

from database.connection import SessionFactory
from user.models import User
from user.request import UserCreateRequest, UserUpdateRequest
from user.response import UserResponse

# 아래의 user 핸들러 함수들을 관리하는 객체
# router = APIRouter(prefix="/users")
router = APIRouter(tags=["User"])

# 임시 데이터
users = [
        {"id": 1, "name": "alex", "job": "student"},
        {"id": 2, "name": "bob", "job": "sw engineer"},
        {"id": 3, "name": "chris", "job": "barista"},
    ]

# 전체 사용자 조회 API
@router.get("/users", status_code=status.HTTP_200_OK)
def get_users_handler():
    return users

# 주의!! 순서가 매우 중요(동적 변수보다 위에 있어야 실행됨)
# query parameter
@router.get("/users/search")
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
@router.get("/users/{user_id}")
def get_user_one_handler(
    # user_id: int
    # ge: 이상(= Greater than or Equal to), le: 이하, max_digits=6: 최대 자릿수 6
    user_id: int = Path(..., ge=1),
):
    for user in users:
        if user["id"] == user_id:
            return user
        # 없는 번호가 입력되면 None 반환 & 404 에러 반환
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User Not Found",
    )

# 회원 추가 API
# POST /users
@router.post(
    "/users", 
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse
)
def create_user_handler(
    # 1) 사용자 데이터를 넘겨 받는다 + 유효성 검사
    body: UserCreateRequest
):
    # 2) 사용자 데이터를 저장한다
    session = SessionFactory()

    # context manager를 벗어나는 순간 자동으로 close() 호출
    with SessionFactory() as session:
        new_user = User(name=body.name, job=body.job)
        session.add(new_user)
        session.commit()    # 변경사항 저장
        session.refresh(new_user)    # db로부터 id, created_at 받아옴 (동기화)
        # 3) 응답을 반환한다
        return new_user

# 회원 정보 수정 API    (PUT: 전체 교체(replace), PATCH: 일부 수정(partial update))
@router.patch(
        "/users/{user_id}",
        response_model=UserResponse,
        )
def update_user_handler(
    # 1) 클라이언트로부터 수정할 데이터(사용자 id, 변경할 값)를 넘겨 받는다
    user_id: int,
    body: UserUpdateRequest,
):
    # 2) 처리
    # 2-1) user_id로 사용자 조회
    for user in users:
        if user["id"] == user_id:
            # 2-2) 수정
            user["job"] = body.job
            # 3) 반환
            return user
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User Not Found",
    )

# 회원 삭제 API
@router.delete(
        "/users/{user_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        )
def delete_user_handler(user_id: int):
    for user in users:
        if user["id"] == user_id:
            users.remove(user)
            return {"msg": "user deleted..."}    # 이렇게 반환할걸 적어둬도 위의 status 때문에 반환 안됨. 쓰고싶으면 코드 바꿔야...
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User Not Found",
    )