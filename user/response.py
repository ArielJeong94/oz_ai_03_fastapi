# 응답 데이터의 형식 관리
# 1) 클라이언트에게 잘못된 데이터를 반환하지 않기 위해 사용
# 2) 민감 데이터(개인정보)를 실수로 유출하지 않기 위해 사용
from datetime import datetime
from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    name: str
    job: str
    created_at: datetime