# 요청 본문의 데이터 형식 관리 파일
from pydantic import BaseModel, Field


# 사용자 추가할 때 데이터 형식
class UserCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=10)   # 2~10글자로 제한
    job: str

# 사용자 데이터를 수정할 때 데이터 형식
class UserUpdateRequest(BaseModel):
    job: str