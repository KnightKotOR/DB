from pydantic import BaseModel
from typing import List


class MetadataRequest(BaseModel):
    databases: List[str]

class MetadataResponse(BaseModel):
    status: str
    message: str