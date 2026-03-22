from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.schemas import ProductResponse, ProductCreate
from app.repository.repository import ProductRepository
from app.api.v1.auth import get_current_user

router = APIRouter(prefix="/products", tags=["Produtos"])

@router.get("/", response_model=List[ProductResponse], summary="Listar todos os produtos")
def get_products(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    product_repo = ProductRepository(db)
    return product_repo.get_all(skip=skip, limit=limit)

@router.get("/{product_id}", response_model=ProductResponse, summary="Obter detalhes de um produto")
def get_product(
    product_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    product_repo = ProductRepository(db)
    product = product_repo.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED, summary="Criar novo produto")
def create_product(
    product_in: ProductCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    product_repo = ProductRepository(db)
    return product_repo.create(product_in)

@router.put("/{product_id}", response_model=ProductResponse, summary="Atualizar produto existente")
def update_product(
    product_id: int, 
    product_in: ProductCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    product_repo = ProductRepository(db)
    product = product_repo.update(product_id, product_in)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Remover um produto")
def delete_product(
    product_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    product_repo = ProductRepository(db)
    if not product_repo.delete(product_id):
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return None
