from fastapi import FastAPI
from controllers import auth_controller
from contextlib import asynccontextmanager
from services.redis_service import RedisService
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        RedisService()
    except Exception:
        sys.exit("Cannot start server because Redis is unreachable")
    yield 

app = FastAPI(title="confido-auth", lifespan=lifespan)
app.include_router(auth_controller.router)

@app.get("/health")
def health():
    return {"status": "ok"}