from fastapi import APIRouter, HTTPException
from typing import List
from models.query_model import QueryRequest, QueryResponse
from services.query_service import execute_query

router = APIRouter(tags=["Query"])

@router.post("/query", response_model=QueryResponse)
def execute_query_on_server(qr: QueryRequest):
    """Returns list of databases."""
    return execute_query(qr)

