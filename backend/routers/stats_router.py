from fastapi import APIRouter, HTTPException
from models.stats_model import StatCount
from services.stats_service import (get_table_count_by_db, get_column_count_by_db, get_primary_key_count_by_db,
                                            get_foreign_key_count_by_db, get_unique_key_count_by_db,
                                            get_record_count_by_db)

router = APIRouter(tags=["Statistics"])

@router.get("/databases/{db_id}/tables/count", response_model=StatCount)
def get_table_count(db_id: int):
    """
    Returns number of tables in specified database (using db_id).
    """
    try:
        return get_table_count_by_db(db_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/databases/{db_id}/columns/count", response_model=StatCount)
def get_column_count(db_id: int):
    """
     Returns number of columns in specified database (using db_id).
    """
    try:
        return get_column_count_by_db(db_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/databases/{db_id}/keys/primary/count", response_model=StatCount)
def get_pk_count(db_id: int):
    """
     Returns number of primary keys in specified database (using db_id).
    """
    try:
        return get_primary_key_count_by_db(db_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/databases/{db_id}/keys/foreign/count", response_model=StatCount)
def get_fk_count(db_id: int):
    """
     Returns number of foreign keys in specified database (using db_id).
    """
    try:
        return get_foreign_key_count_by_db(db_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/databases/{db_id}/keys/unique/count", response_model=StatCount)
def get_uk_count(db_id: int):
    """
     Returns number of unique keys in specified database (using db_id).
    """
    try:
        return get_unique_key_count_by_db(db_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/databases/{db_id}/records/count", response_model=StatCount)
def get_record_count(db_id: int):
    """
     Returns number of records in specified database (using db_id).
    """
    try:
        return get_record_count_by_db(db_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))