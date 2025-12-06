from pydantic import BaseModel
from typing import List

class QueryRequest(BaseModel):
    database: str
    table: str
    column: str

class QueryResponse(BaseModel):
    column: str
    info: List[str]