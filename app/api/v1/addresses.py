from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.schemas import AddressResponse, AddressCreate
from app.repository.repository import AddressRepository
from app.services.viacep import ViaCEPService
from app.api.v1.auth import get_current_user

router = APIRouter(prefix="/addresses", tags=["Endereços"])

@router.get("/", response_model=List[AddressResponse], summary="Listar todos os endereços")
def get_addresses(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    address_repo = AddressRepository(db)
    return address_repo.get_all(skip=skip, limit=limit)

@router.get("/cep/{cep}", summary="Consultar endereço via CEP")
async def get_address_by_cep(
    cep: str,
    current_user = Depends(get_current_user)
):
    viacep = ViaCEPService()
    address_data = await viacep.get_address_by_cep(cep)
    if not address_data:
        raise HTTPException(status_code=404, detail="CEP não encontrado")
    return address_data

@router.post("/", response_model=AddressResponse, status_code=status.HTTP_201_CREATED, summary="Criar novo endereço")
def create_address(
    address_in: AddressCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    address_repo = AddressRepository(db)
    return address_repo.create(address_in)

@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Remover um endereço")
def delete_address(
    address_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    address_repo = AddressRepository(db)
    if not address_repo.delete(address_id):
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return None
