from typing import List
from fastapi import APIRouter, HTTPException
from schemas import CircularDetail, CircularSummary
from services.circulars import get_circular_document, load_circular_documents


router = APIRouter(prefix="/circulars", tags=["circulars"])


@router.get("", response_model=List[CircularSummary])
def list_circulars() -> List[CircularSummary]:
    documents = load_circular_documents()
    return [
        CircularSummary(id=document.id, title=document.title)
        for document in documents
    ]


@router.get("/{circular_id}", response_model=CircularDetail)
def get_circular(circular_id: str) -> CircularDetail:
    document = get_circular_document(circular_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Circular not found")

    return CircularDetail(
        id=document.id,
        title=document.title,
        content=document.content,
    )