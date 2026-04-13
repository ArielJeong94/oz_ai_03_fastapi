import anyio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from user.router import router

# 쓰레드 풀 크기 조정
@asynccontextmanager
async def lifespan(_):
    limiter = anyio.to_thread.current_default_thread_limiter()
    limiter.total_tokens = 200
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router)

# 만약 비동기함수 안에 동기함수를 써야만 하는 상황(비동기 라이브러리를 지원하지 않는 경우)인 경우
from starlette.concurrency import run_in_threadpool

def aws_sync():
    # AWS 서버랑 통신 (예: 2초)
    return

@ app.get("/async")
async def async_handler():
    await run_in_threadpool(aws_sync)
    return {"msg": "ok"}