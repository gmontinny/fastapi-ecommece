from sqlalchemy.orm import Session
from app.models.models import User, Product, Category, Customer, Supplier, Address, Tag, Coupon, SalesOrder, ProductStatus
from app.schemas.schemas import UserCreate, UserUpdate, ProductCreate, CategoryCreate, CustomerCreate, SupplierCreate, AddressCreate, TagBase, CouponBase, ProductStatusBase
from app.core.security import get_password_hash

class BaseRepository:
    def __init__(self, db: Session):
        self.db = db

class UserRepository(BaseRepository):
    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(User).offset(skip).limit(limit).all()

    def get_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def create(self, user_in: UserCreate):
        db_user = User(
            email=user_in.email,
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            hashed_password=get_password_hash(user_in.password)
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, user_id: int, user_in: UserUpdate):
        db_user = self.get_by_id(user_id)
        if db_user:
            update_data = user_in.model_dump(exclude_unset=True)
            if "password" in update_data:
                update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
            for key, value in update_data.items():
                setattr(db_user, key, value)
            self.db.commit()
            self.db.refresh(db_user)
        return db_user

    def delete(self, user_id: int):
        db_user = self.get_by_id(user_id)
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
            return True
        return False

class ProductRepository(BaseRepository):
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Product).offset(skip).limit(limit).all()

    def get_by_id(self, product_id: int):
        return self.db.query(Product).filter(Product.id == product_id).first()

    def create(self, product_in: ProductCreate):
        db_product = Product(**product_in.model_dump())
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def update(self, product_id: int, product_in: ProductCreate):
        db_product = self.get_by_id(product_id)
        if db_product:
            for key, value in product_in.model_dump().items():
                setattr(db_product, key, value)
            self.db.commit()
            self.db.refresh(db_product)
        return db_product

    def delete(self, product_id: int):
        db_product = self.get_by_id(product_id)
        if db_product:
            self.db.delete(db_product)
            self.db.commit()
            return True
        return False

class CategoryRepository(BaseRepository):
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Category).offset(skip).limit(limit).all()

    def get_by_id(self, category_id: int):
        return self.db.query(Category).filter(Category.id == category_id).first()

    def create(self, category_in: CategoryCreate):
        db_category = Category(**category_in.model_dump())
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category)
        return db_category

    def update(self, category_id: int, category_in: CategoryCreate):
        db_category = self.get_by_id(category_id)
        if db_category:
            for key, value in category_in.model_dump().items():
                setattr(db_category, key, value)
            self.db.commit()
            self.db.refresh(db_category)
        return db_category

    def delete(self, category_id: int):
        db_category = self.get_by_id(category_id)
        if db_category:
            self.db.delete(db_category)
            self.db.commit()
            return True
        return False

class CustomerRepository(BaseRepository):
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Customer).offset(skip).limit(limit).all()

    def get_by_id(self, customer_id: int):
        return self.db.query(Customer).filter(Customer.id == customer_id).first()

    def create(self, customer_in: CustomerCreate):
        db_customer = Customer(**customer_in.model_dump())
        self.db.add(db_customer)
        self.db.commit()
        self.db.refresh(db_customer)
        return db_customer

    def update(self, customer_id: int, customer_in: CustomerCreate):
        db_customer = self.get_by_id(customer_id)
        if db_customer:
            for key, value in customer_in.model_dump().items():
                setattr(db_customer, key, value)
            self.db.commit()
            self.db.refresh(db_customer)
        return db_customer

    def delete(self, customer_id: int):
        db_customer = self.get_by_id(customer_id)
        if db_customer:
            self.db.delete(db_customer)
            self.db.commit()
            return True
        return False

class SupplierRepository(BaseRepository):
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Supplier).offset(skip).limit(limit).all()

    def get_by_id(self, supplier_id: int):
        return self.db.query(Supplier).filter(Supplier.id == supplier_id).first()

    def create(self, supplier_in: SupplierCreate):
        db_supplier = Supplier(**supplier_in.model_dump())
        self.db.add(db_supplier)
        self.db.commit()
        self.db.refresh(db_supplier)
        return db_supplier

    def update(self, supplier_id: int, supplier_in: SupplierCreate):
        db_supplier = self.get_by_id(supplier_id)
        if db_supplier:
            for key, value in supplier_in.model_dump().items():
                setattr(db_supplier, key, value)
            self.db.commit()
            self.db.refresh(db_supplier)
        return db_supplier

    def delete(self, supplier_id: int):
        db_supplier = self.get_by_id(supplier_id)
        if db_supplier:
            self.db.delete(db_supplier)
            self.db.commit()
            return True
        return False

class AddressRepository(BaseRepository):
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Address).offset(skip).limit(limit).all()

    def get_by_id(self, address_id: int):
        return self.db.query(Address).filter(Address.id == address_id).first()

    def create(self, address_in: AddressCreate):
        db_address = Address(**address_in.model_dump())
        self.db.add(db_address)
        self.db.commit()
        self.db.refresh(db_address)
        return db_address

    def update(self, address_id: int, address_in: AddressCreate):
        db_address = self.get_by_id(address_id)
        if db_address:
            for key, value in address_in.model_dump().items():
                setattr(db_address, key, value)
            self.db.commit()
            self.db.refresh(db_address)
        return db_address

    def delete(self, address_id: int):
        db_address = self.get_by_id(address_id)
        if db_address:
            self.db.delete(db_address)
            self.db.commit()
            return True
        return False

class TagRepository(BaseRepository):
    def get_all(self):
        return self.db.query(Tag).all()

    def create(self, tag_in: TagBase):
        db_tag = Tag(**tag_in.model_dump())
        self.db.add(db_tag)
        self.db.commit()
        self.db.refresh(db_tag)
        return db_tag

class CouponRepository(BaseRepository):
    def get_all(self):
        return self.db.query(Coupon).all()

    def get_by_code(self, code: str):
        return self.db.query(Coupon).filter(Coupon.code == code, Coupon.active == True).first()

    def create(self, coupon_in: CouponBase):
        db_coupon = Coupon(**coupon_in.model_dump())
        self.db.add(db_coupon)
        self.db.commit()
        self.db.refresh(db_coupon)
        return db_coupon

class SalesOrderRepository(BaseRepository):
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(SalesOrder).offset(skip).limit(limit).all()

    def get_by_id(self, order_id: int):
        return self.db.query(SalesOrder).filter(SalesOrder.id == order_id).first()

    def create(self, order_data: dict):
        db_order = SalesOrder(**order_data)
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return db_order

class ProductStatusRepository(BaseRepository):
    def get_all(self):
        return self.db.query(ProductStatus).all()

    def create(self, status_in: ProductStatusBase):
        db_status = ProductStatus(**status_in.model_dump())
        self.db.add(db_status)
        self.db.commit()
        self.db.refresh(db_status)
        return db_status
