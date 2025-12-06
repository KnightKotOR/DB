from pydantic import BaseModel

class DatabaseItem(BaseModel):
    db_id: int
    db_name: str