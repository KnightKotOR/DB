from fastapi import APIRouter
from typing import List
from models.md_model import MetadataRequest, MetadataResponse
from services.md_service import collect_metadata

router = APIRouter(tags=["Metadata"])

@router.post("/metadata/import")
def import_metadata(request: MetadataRequest) -> List[MetadataResponse]:
    """Imports information of specified databases into metadata_catalog."""
    results = []
    for db_name in request.databases:
        result = collect_metadata(db_name)
        results.append(result)
    return results