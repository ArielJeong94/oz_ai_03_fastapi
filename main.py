from fastapi import FastAPI
from user.router import router

app = FastAPI()
app.include_router(router)



@app.get("/sync")
def sync_handler():
    import time
    time.sleep(5)
    return {"msg": "ok"}