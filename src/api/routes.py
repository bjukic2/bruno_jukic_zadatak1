from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse
from typing import Optional
from src.services.tickets import fetch_tickets, compute_stats
import httpx
import logging
import os
from utils.limiter import limiter

logger = logging.getLogger(__name__)

router = APIRouter()

#implementacija različitih GET i POST endopointova
@router.get("/tickets") #GET endpoint za prikazivanje ticketsa po različitih filterima
@limiter.limit("10/minute")
async def get_tickets(
    request: Request,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    description: Optional[str] = None,
    page: int = 1,
    size: int = 10
):
    logger.info(f"GET /tickets called with status={status}, priority={priority}, description={description}, page={page}, size={size}")
    tickets = await fetch_tickets()
    if status:
        tickets = [t for t in tickets if t.status == status]
    if priority:
        tickets = [t for t in tickets if t.priority == priority]
    if description:
        tickets = [t for t in tickets if description.lower() in t.title.lower()]
    start = (page - 1) * size
    return tickets[start:start+size]


@router.get("/tickets/{ticket_id}") #GET endpoint za prikaz ticketsa po id-u
async def get_ticket_by_id(ticket_id: int):
    logger.info(f"GET /tickets/{ticket_id} called")
    tickets = await fetch_tickets()
    ticket = next((t for t in tickets if t.id == ticket_id), None)
    if ticket:
        return ticket
    logger.warning(f"Ticket with id {ticket_id} not found")
    return {"error": "Ticket not found"}

@router.get("/stats") #GET endpoint za prikazivanje stats
async def stats():
    logger.info("GET /stats called")
    return await compute_stats()

@router.get("/health") #GET endpoint za prikazivanje health
async def health_check():
    logger.info("GET /health called")
    return {"status": "ok"}

DUMMYJSON_LOGIN_URL = "https://dummyjson.com/auth/login"

@router.post("/auth/login") #POST endpoint za autorizaciju
async def login(username: str, password: str):
    logger.info(f"POST /auth/login called with username={username}")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(DUMMYJSON_LOGIN_URL, json={"username": username, "password": password})
        except httpx.HTTPError as e:
            logger.error(f"HTTP error during login: {e}")

        if response.status_code != 200:
            logger.warning(f"Failed login attempt for user: {username}")
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        logger.info(f"User {username} logged in successfully")
        return response.json()
    
@router.get("/", include_in_schema=False) #GET endpoint za prikaz static html
async def serve_redoc():
    path = os.path.abspath("static/docs.html")
    if not os.path.exists(path):
        raise HTTPException(status_code=500, detail="Documentation file not found.")
    return FileResponse(path, media_type="text/html")