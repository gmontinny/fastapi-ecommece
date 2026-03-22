from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)

class UserResponse(UserBase):
    id: int
    active: bool
    inserted_at: datetime

    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Product Schemas
class ProductBase(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    regular_price: Decimal = Field(default=0, ge=0)
    discount_price: Decimal = Field(default=0, ge=0)
    quantity: int = Field(default=0, ge=0)
    taxable: bool = False
    product_status_id: int

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    inserted_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Address Schemas
class AddressBase(BaseModel):
    cep: str = Field(..., pattern=r"^\d{5}-?\d{3}$")
    street: str
    complement: Optional[str] = None
    neighborhood: str
    city: str
    state: str = Field(..., min_length=2, max_length=2)
    number: str

class AddressCreate(AddressBase):
    customer_id: Optional[int] = None
    supplier_id: Optional[int] = None

class AddressResponse(AddressBase):
    id: int
    inserted_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Customer Schemas
class CustomerBase(BaseModel):
    full_name: str
    cpf: str = Field(..., pattern=r"^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$")
    email: EmailStr
    phone: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: int
    addresses: List[AddressResponse] = []
    inserted_at: datetime

    class Config:
        from_attributes = True

# Supplier Schemas
class SupplierBase(BaseModel):
    corporate_name: str
    cnpj: str = Field(..., pattern=r"^\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}$")
    email: EmailStr
    contact_name: Optional[str] = None

class SupplierCreate(SupplierBase):
    pass

class SupplierResponse(SupplierBase):
    id: int
    addresses: List[AddressResponse] = []
    inserted_at: datetime

    class Config:
        from_attributes = True

# Category Schemas
class CategoryBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    inserted_at: datetime

    class Config:
        from_attributes = True

# Tag Schemas
class TagBase(BaseModel):
    name: str

class TagResponse(TagBase):
    id: int
    inserted_at: datetime

    class Config:
        from_attributes = True

# Product Status Schemas
class ProductStatusBase(BaseModel):
    name: str

class ProductStatusResponse(ProductStatusBase):
    id: int
    inserted_at: datetime

    class Config:
        from_attributes = True

# Coupon Schemas
class CouponBase(BaseModel):
    code: str
    description: Optional[str] = None
    active: bool = True
    value: Decimal
    multiple: bool = False
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class CouponResponse(CouponBase):
    id: int
    inserted_at: datetime

    class Config:
        from_attributes = True
