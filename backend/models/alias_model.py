from pydantic import BaseModel


class AliasRequest(BaseModel):
    database: str
    table: str
    alias: str

class AliasResponse(BaseModel):
    message: str
