from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from enum import Enum


class CreatedModel(BaseModel):
    created_id: int

class StatusModel(BaseModel):
    status: bool


class UserRole(str, Enum):
    BUYER = "buyer"
    SELLER = "seller"
    ADMIN = "admin"

class ActiveModel(BaseModel):
    role: UserRole
    username: str
    is_active: bool

class UserActive(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.BUYER

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    password_hash: str
    created_at: datetime
    role: UserRole
    is_active: bool
    company_name: Optional[str]
    tax_id: Optional[str]
    phone_number: Optional[str]

class UserSeller(BaseModel):
    id: int
    company_name: str
    tax_id: str
    phone_number: str

class UserRequestUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    company_name: Optional[str] = None
    tax_id: Optional[str] = None


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int = 0
    seller_id: int
    category_id: int

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float = Field(ge=0)
    stock: int
    seller_id: int
    category_id: int
    created_at: datetime

class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[int]
    stock: Optional[int]


class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class OrderCreate(BaseModel):
    buyer_id: int
    total_amount: float = Field(ge=0)
    shipping_address_id: int

class OrderItemCreate(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    price_at_purchase: float

class OrderResponse(BaseModel):
    id: int
    buyer_id: int
    total_amount: float
    status: OrderStatus
    created_at: datetime

class OrderItemResponse(BaseModel):
    id: int
    quantity: int
    price_at_purchase: float
    order_id: int
    product_id: int


class ReviewCreate(BaseModel):
    user_id: int
    product_id: int
    rating: int = Field(ge=1, le=5)
    comment: str

class ReviewResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    rating: int
    comment: str
    created_at: datetime


class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class PaymentCreate(BaseModel):
    order_id: int
    amount: float = Field(ge=0)
    payment_method: str
    transaction_id: str

class PaymentResponse(BaseModel):
    id: int
    order_id: int
    amount: float
    payment_method: str
    status: PaymentStatus
    created_at: datetime


class CreateCategory(BaseModel):
    name: str
    parent_id: Optional[int] = None

class UpdateCategory(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[int] = None

class CategoryResponse(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]


class CartItemUpdate(BaseModel):
    cart_id: int
    product_id: int
    quantity: int