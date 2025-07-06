from pydantic import BaseModel
from typing import Literal

class Ticket(BaseModel):
    id: int
    title: str
    status: Literal["open", "closed"] = None
    priority: Literal["low", "medium", "high"] = None
    assignee: str
    description: str = ""
    full_json: dict = {}

