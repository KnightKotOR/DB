from pydantic import BaseModel

class StatCount(BaseModel):
    db_id: int
    count: int