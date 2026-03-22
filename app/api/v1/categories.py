from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.schemas import CategoryResponse, CategoryCreate
from app.repository.repository import CategoryRepository
from app.api.v1.auth import get_current_user

router = APIRouter(prefix="/categories", tags=["Categorias"])

@router.get("/", response_model=List[CategoryResponse], summary="Listar todas as categorias")
def get_categories(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    category_repo = CategoryRepository(db)
    return category_repo.get_all(skip=skip, limit=limit)

@router.get("/{category_id}", response_model=CategoryResponse, summary="Obter detalhes de uma categoria")
def get_category(
    category_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    category_repo = CategoryRepository(db)
    category = category_repo.get_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return category

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED, summary="Criar nova categoria")
def create_category(
    category_in: CategoryCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    category_repo = CategoryRepository(db)
    return category_repo.create(category_in)

@router.put("/{category_id}", response_model=CategoryResponse, summary="Atualizar categoria existente")
def update_category(
    category_id: int, 
    category_in: CategoryCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    category_repo = CategoryRepository(db)
    category = category_repo.update(category_id, category_in)
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Remover uma categoria")
def delete_category(
    category_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    category_repo = CategoryRepository(db)
    if not category_repo.delete(category_id):
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return None
