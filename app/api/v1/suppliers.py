from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.schemas import SupplierResponse, SupplierCreate
from app.repository.repository import SupplierRepository
from app.api.v1.auth import get_current_user

router = APIRouter(prefix="/suppliers", tags=["Fornecedores"])

@router.get("/", response_model=List[SupplierResponse], summary="Listar todos os fornecedores")
def get_suppliers(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    supplier_repo = SupplierRepository(db)
    return supplier_repo.get_all(skip=skip, limit=limit)

@router.get("/{supplier_id}", response_model=SupplierResponse, summary="Obter detalhes de um fornecedor")
def get_supplier(
    supplier_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    supplier_repo = SupplierRepository(db)
    supplier = supplier_repo.get_by_id(supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    return supplier

@router.post("/", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED, summary="Criar novo fornecedor")
def create_supplier(
    supplier_in: SupplierCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    supplier_repo = SupplierRepository(db)
    return supplier_repo.create(supplier_in)

@router.put("/{supplier_id}", response_model=SupplierResponse, summary="Atualizar fornecedor existente")
def update_supplier(
    supplier_id: int, 
    supplier_in: SupplierCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    supplier_repo = SupplierRepository(db)
    supplier = supplier_repo.update(supplier_id, supplier_in)
    if not supplier:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    return supplier

@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Remover um fornecedor")
def delete_supplier(
    supplier_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    supplier_repo = SupplierRepository(db)
    if not supplier_repo.delete(supplier_id):
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    return None
