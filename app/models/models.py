from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric, Text, Date, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

# Association Tables
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
    Column("inserted_at", DateTime(timezone=True), default=datetime.utcnow, nullable=False),
    Column("updated_at", DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False),
)

product_tags = Table(
    "product_tags",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
    Column("inserted_at", DateTime(timezone=True), default=datetime.utcnow, nullable=False),
    Column("updated_at", DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False),
)

product_categories = Table(
    "product_categories",
    Base.metadata,
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True),
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
    Column("inserted_at", DateTime(timezone=True), default=datetime.utcnow, nullable=False),
    Column("updated_at", DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False),
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False) # Adicionado para auth
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    active = Column(Boolean, default=True)
    inserted_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    roles = relationship("Role", secondary=user_roles, back_populates="users")
    orders = relationship("SalesOrder", back_populates="user")

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    inserted_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    users = relationship("User", secondary=user_roles, back_populates="roles")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    inserted_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    products = relationship("Product", secondary=product_categories, back_populates="categories")
    subcategories = relationship("Category")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(255), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    product_status_id = Column(Integer, ForeignKey("product_statuses.id"), nullable=False)
    regular_price = Column(Numeric, default=0)
    discount_price = Column(Numeric, default=0)
    quantity = Column(Integer, default=0)
    taxable = Column(Boolean, default=False)
    inserted_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    status = relationship("ProductStatus", back_populates="products")
    categories = relationship("Category", secondary=product_categories, back_populates="products")
    tags = relationship("Tag", secondary=product_tags, back_populates="products")

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    inserted_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    products = relationship("Product", secondary=product_tags, back_populates="tags")

class ProductStatus(Base):
    __tablename__ = "product_statuses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    inserted_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    products = relationship("Product", back_populates="status")

class SalesOrder(Base):
    __tablename__ = "sales_orders"
    id = Column(Integer, primary_key=True, index=True)
    order_date = Column(Date, nullable=False, default=datetime.utcnow)
    total = Column(Numeric, nullable=False)
    coupon_id = Column(Integer, ForeignKey("coupons.id"), nullable=True)
    session_id = Column(String(255), ForeignKey("sessions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    inserted_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="orders")
    coupon = relationship("Coupon")
    session = relationship("Session")
    order_products = relationship("OrderProduct", back_populates="order")

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20))
    inserted_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    addresses = relationship("Address", back_populates="customer")

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    corporate_name = Column(String(255), nullable=False) # Razão Social
    cnpj = Column(String(18), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False)
    contact_name = Column(String(255))
    inserted_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    addresses = relationship("Address", back_populates="supplier")

class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    cep = Column(String(9), nullable=False)
    street = Column(String(255), nullable=False)
    complement = Column(String(255))
    neighborhood = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    state = Column(String(2), nullable=False)
    number = Column(String(20), nullable=False)
    
    # Relacionamentos opcionais (pode pertencer a um cliente ou fornecedor)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
    
    inserted_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    customer = relationship("Customer", back_populates="addresses")
    supplier = relationship("Supplier", back_populates="addresses")

class Coupon(Base):
    __tablename__ = "coupons"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    active = Column(Boolean, default=True)
    value = Column(Numeric)
    multiple = Column(Boolean, default=False)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    inserted_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class Session(Base):
    __tablename__ = "sessions"
    id = Column(String(255), primary_key=True)
    data = Column(Text)
    inserted_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class OrderProduct(Base):
    __tablename__ = "order_products"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("sales_orders.id"))
    sku = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Numeric, nullable=False)
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Numeric, nullable=False)
    inserted_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    order = relationship("SalesOrder", back_populates="order_products")
