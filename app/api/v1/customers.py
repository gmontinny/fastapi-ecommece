from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.schemas import CustomerResponse, CustomerCreate
from app.repository.repository import CustomerRepository
from app.api.v1.auth import get_current_user

router = APIRouter(prefix="/customers", tags=["Clientes"])

@router.get("/", response_model=List[CustomerResponse], summary="Listar todos os clientes")
def get_customers(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    customer_repo = CustomerRepository(db)
    return customer_repo.get_all(skip=skip, limit=limit)

@router.get("/{customer_id}", response_model=CustomerResponse, summary="Obter detalhes de um cliente")
def get_customer(
    customer_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    customer_repo = CustomerRepository(db)
    customer = customer_repo.get_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return customer

@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED, summary="Criar novo cliente")
def create_customer(
    customer_in: CustomerCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    customer_repo = CustomerRepository(db)
    return customer_repo.create(customer_in)

@router.put("/{customer_id}", response_model=CustomerResponse, summary="Atualizar cliente existente")
def update_customer(
    customer_id: int, 
    customer_in: CustomerCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    customer_repo = CustomerRepository(db)
    customer = customer_repo.update(customer_id, customer_in)
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return customer

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Remover um cliente")
def delete_customer(
    customer_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    customer_repo = CustomerRepository(db)
    if not customer_repo.delete(customer_id):
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return None
