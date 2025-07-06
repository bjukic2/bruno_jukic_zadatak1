import httpx
import logging
from src.models.ticket import Ticket
from collections import Counter
import redis.asyncio as redis
import os
import json

logger = logging.getLogger(__name__)

PRIORITIES = {0: "low", 1: "medium", 2: "high"}
TODOS_URL = "https://dummyjson.com/todos"
USERS_URL = "https://dummyjson.com/users"

_cached_users = None

# Redis client init
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

CACHE_TICKETS_KEY = "tickets_cache"
CACHE_STATS_KEY = "stats_cache"
CACHE_TTL = 60  # u sekundama

async def get_users():
    global _cached_users
    if _cached_users is not None:
        logger.info("Using cached users")
        return _cached_users

    logger.info("Fetching users from DummyJSON")
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(USERS_URL)
            resp.raise_for_status()
        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch users: {e}")
            raise RuntimeError("Failed to fetch users") from e

    _cached_users = {u["id"]: u["username"] for u in resp.json()["users"]}
    logger.info(f"Fetched {len(_cached_users)} users")
    return _cached_users


async def fetch_tickets():
    cached = await redis_client.get(CACHE_TICKETS_KEY)
    if cached:
        logger.info("Using cached tickets from Redis")
        tickets_data = json.loads(cached)
        return [Ticket(**t) for t in tickets_data]

    logger.info("Fetching tickets from DummyJSON")
    async with httpx.AsyncClient() as client:
        try:
            todos_resp = await client.get(TODOS_URL)
            todos_resp.raise_for_status()
        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch todos: {e}")
            raise RuntimeError("Failed to fetch todos") from e

        todos = todos_resp.json()["todos"]

    users = await get_users()

    tickets = []
    for todo in todos:
        t = Ticket(
            id=todo["id"],
            title=todo["todo"],
            status="closed" if todo["completed"] else "open",
            priority=PRIORITIES[todo["id"] % 3],
            assignee=users.get(todo["userId"], "unknown"),
            description=todo["todo"][:100],
            full_json=todo
        )
        tickets.append(t)

    # Cache to Redis
    tickets_json = [t.dict() for t in tickets]  # pretpostavljam da Ticket ima .dict()
    await redis_client.set(CACHE_TICKETS_KEY, json.dumps(tickets_json), ex=CACHE_TTL)

    logger.info(f"Fetched {len(tickets)} tickets")
    return tickets


async def compute_stats():
    cached = await redis_client.get(CACHE_STATS_KEY)
    if cached:
        logger.info("Using cached stats from Redis")
        return json.loads(cached)

    logger.info("Computing ticket stats")
    tickets = await fetch_tickets()
    status_counts = Counter(t.status for t in tickets)
    priority_counts = Counter(t.priority for t in tickets)
    stats = {
        "total": len(tickets),
        "by_status": status_counts,
        "by_priority": priority_counts
    }
    # Cache stats
    await redis_client.set(CACHE_STATS_KEY, json.dumps(stats), ex=CACHE_TTL)

    return stats
