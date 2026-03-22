from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.schemas import CouponResponse, CouponBase
from app.repository.repository import CouponRepository
from app.api.v1.auth import get_current_user

router = APIRouter(prefix="/coupons", tags=["Cupons"])

@router.get("/", response_model=List[CouponResponse], summary="Listar todos os cupons")
def get_coupons(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    coupon_repo = CouponRepository(db)
    return coupon_repo.get_all()

@router.get("/{code}", response_model=CouponResponse, summary="Obter detalhes de um cupom pelo código")
def get_coupon(
    code: str, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    coupon_repo = CouponRepository(db)
    coupon = coupon_repo.get_by_code(code)
    if not coupon:
        raise HTTPException(status_code=404, detail="Cupom não encontrado ou inativo")
    return coupon

@router.post("/", response_model=CouponResponse, status_code=status.HTTP_201_CREATED, summary="Criar novo cupom")
def create_coupon(
    coupon_in: CouponBase, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    coupon_repo = CouponRepository(db)
    return coupon_repo.create(coupon_in)
