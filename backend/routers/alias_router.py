from fastapi import APIRouter, HTTPException
from typing import List
from models.alias_model import AliasRequest, AliasResponse
from services.alias_service import create_alias, delete_alias

router = APIRouter(tags=["Alias"])

@router.get("/alias/create", response_model=AliasResponse)
def create_alias_on_server(ar: AliasRequest):
    """Creates alias of the db/table name"""
    return create_alias(ar)

@router.get("/alias/delete", response_model=AliasResponse)
def delete_alias_on_server(ar: AliasRequest):
    """Creates alias of the db/table name"""
    return delete_alias(ar)

