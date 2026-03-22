from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.schemas import TagResponse, TagBase, ProductStatusResponse, ProductStatusBase
from app.repository.repository import TagRepository, ProductStatusRepository
from app.api.v1.auth import get_current_user

router = APIRouter(prefix="/metadata", tags=["Metadados"])

@router.get("/tags", response_model=List[TagResponse], summary="Listar todas as tags")
def get_tags(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tag_repo = TagRepository(db)
    return tag_repo.get_all()

@router.post("/tags", response_model=TagResponse, status_code=status.HTTP_201_CREATED, summary="Criar nova tag")
def create_tag(tag_in: TagBase, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    tag_repo = TagRepository(db)
    return tag_repo.create(tag_in)

@router.get("/product-statuses", response_model=List[ProductStatusResponse], summary="Listar todos os status de produto")
def get_statuses(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    status_repo = ProductStatusRepository(db)
    return status_repo.get_all()

@router.post("/product-statuses", response_model=ProductStatusResponse, status_code=status.HTTP_201_CREATED, summary="Criar novo status de produto")
def create_status(status_in: ProductStatusBase, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    status_repo = ProductStatusRepository(db)
    return status_repo.create(status_in)
