# 요청 본문의 데이터 형식 관리 파일
from pydantic import BaseModel, Field


class UserCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=10)   # 2~10글자로 제한
    job: str

