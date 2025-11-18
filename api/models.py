from pydantic import BaseModel
from enum import Enum

class LikedOrFlagged(str, Enum):
    liked = "liked"
    flagged = "flagged"

class WorkflowQuery(BaseModel):
    query: str

class FlagOutput(BaseModel):
    query: str
    response: str
    flag: LikedOrFlagged
    feedback: str | None = None