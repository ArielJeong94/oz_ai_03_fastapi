from fastapi import APIRouter, Path, Query, status, HTTPException, Depends
from sqlalchemy import select, delete

from database.connection import get_session
from user.models import User
from user.request import UserCreateRequest, UserUpdateRequest
from user.response import UserResponse

# 아래의 user 핸들러 함수들을 관리하는 객체
# router = APIRouter(prefix="/users")
router = APIRouter(tags=["User"])

# 전체 사용자 조회 API
@router.get(
        "/users", 
        summary="전체 사용자 조회 API",
        status_code=status.HTTP_200_OK,
        response_model=list[UserResponse],
        )
def get_users_handler(
    # Depends: FastAPI에서 의존성(get_session)을 자동으로 실행/주입/정리
    session = Depends(get_session),
):
    # stmt: statement = 구문(명령문)
    stmt = select(User)    # SELECT * FROM user# SELECT * FROM user
    result = session.execute(stmt)
    users = result.scalars().all()    # [user1, user2, user3, ...]
    return users

# 주의!! 순서가 매우 중요(동적 변수보다 위에 있어야 실행됨)
# query parameter
@router.get(
        "/users/search",
        summary="사용자 정보 검색 API",
        response_model=list[UserResponse],
        )
def search_users_handler(
    name: str | None = Query(None), 
    job: str | None = Query(None),
    session = Depends(get_session),
):
    if not name and not job:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="검색 조건이 없습니다."
        )
    
    stmt = select(User)
    if name:
        stmt = stmt.where(User.name == name)
    if job:
        stmt = stmt.where(User.job == job)
    
    result = session.execute(stmt)
    users = result.scalars().all()
    return users

# 단일 사용자({}로 변수처리) 데이터 조회 API -> {user_id}번 사용자 데이터 조회
# path parameter
@router.get(
        "/users/{user_id}",
        summary="단일 사용자 데이터 조회 API",
        response_model=UserResponse,
        )
def get_user_one_handler(
    # user_id: int
    # ge: 이상(= Greater than or Equal to), le: 이하, max_digits=6: 최대 자릿수 6
    user_id: int = Path(..., ge=1),
    session = Depends(get_session),
):
    stmt = select(User).where(User.id == user_id)
    result = session.execute(stmt)
    user = result.scalar()    # 존재하면 user 객체, 존재하지 않으면 None

    if not user:
        # 없는 번호가 입력되면 None 반환 & 404 에러 반환
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found",
        )
    return user

# 회원 추가 API
# POST /users
@router.post(
    "/users", 
    summary="회원 추가 API",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse
)
def create_user_handler(
    # 1) 사용자 데이터를 넘겨 받는다 + 유효성 검사
    body: UserCreateRequest,
    session = Depends(get_session),
):
    # 2) 사용자 데이터를 저장한다
    new_user = User(name=body.name, job=body.job)
    session.add(new_user)
    session.commit()    # 변경사항 저장
    session.refresh(new_user)    # db로부터 id, created_at 받아옴 (동기화)
    # 3) 응답을 반환한다
    return new_user

# 회원 정보 수정 API    (PUT: 전체 교체(replace), PATCH: 일부 수정(partial update))
@router.patch(
        "/users/{user_id}",
        summary="회원 정보 수정 API",
        response_model=UserResponse,
        )
def update_user_handler(
    # 1) 클라이언트로부터 수정할 데이터(사용자 id, 변경할 값)를 넘겨 받는다
    user_id: int,
    body: UserUpdateRequest,
    session = Depends(get_session),
):
    stmt = select(User).where(User.id == user_id)
    result = session.execute(stmt)
    user = result.scalar()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found",
        )
        
    user.job = body.job
    session.commit()    # user 상태(job 변경)를 DB 반영
    return user

@router.delete(
        "/users/{user_id}",
        summary="회원 삭제 API",
        status_code=status.HTTP_204_NO_CONTENT,
        )
def delete_user_handler(
    user_id: int,
    session = Depends(get_session),
    ):
    # 방법 1) get + delete
    stmt = select(User).where(User.id == user_id)
    result = session.execute(stmt)
    user = result.scalar()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found",
        )

    session.delete(user)    # 객체를 삭제
    # cf) session.expunge(user) -> 세션의 추적 대상에서 제거
    session.commit()

    # 방법 2) delete
    # stmt = delete(User).where(User.id == user_id)
    # session.execute(stmt)
    # session.commit()