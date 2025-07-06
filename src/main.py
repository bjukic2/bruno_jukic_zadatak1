from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.api.routes import router
import logging
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from utils.limiter import limiter

logging.basicConfig(
    level = logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="TicketHub API")
logger.info("Starting TicketHub API")

app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded."}
    )

app.include_router(router)

