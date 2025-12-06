from fastapi import APIRouter, HTTPException
from typing import List
from models.db_model import DatabaseItem
from services.db_service import get_all_databases, get_database_by_id

router = APIRouter(tags=["Databases"])

@router.get("/databases/", response_model=List[DatabaseItem])
def list_databases():
    """Returns list of databases."""
    return get_all_databases()

@router.get("/database/{db_id}", response_model=DatabaseItem)
def get_database(db_id: int):
    """Returns database with specified id"""
    try:
        return get_database_by_id(db_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))