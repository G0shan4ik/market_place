import enum
import re
from datetime import datetime

from typing import Optional

import bcrypt
from sqlalchemy import ForeignKey, String, BigInteger, Enum, CheckConstraint, Integer
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, validates

from .core import Base


class OrderStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class PaymentStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class UserRole(enum.Enum):
    BUYER = "buyer"
    SELLER = "seller"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger(), autoincrement=True, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(60), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, values_callable=lambda enum_class: [member.value for member in enum_class], create_type=False), nullable=False, default=UserRole.BUYER.value)
    is_active: Mapped[bool] = mapped_column(default=True)

    company_name: Mapped[Optional[str]] = mapped_column(String(100))
    tax_id: Mapped[Optional[str]] = mapped_column(String(20))

    phone_number: Mapped[Optional[str]] = mapped_column(String(20), unique=True)

    @hybrid_property
    def password(self):
        raise AttributeError('Пароль не доступен для чтения')

    @password.setter
    def password(self, password):
        self.set_password(password)

    def set_password(self, password: str) -> None:
        """
            Password Hashing
        :param password: Unencrypted password ( type(str) )
        :return: None
        """
        if not password:
            raise ValueError('Пароль не может быть пустым')

        if len(password) < 8:
            raise ValueError('Пароль должен содержать минимум 8 символов')

        if not re.search(r'[A-Z]', password):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву')

        if not re.search(r'[a-z]', password):
            raise ValueError('Пароль должен содержать хотя бы одну строчную букву')

        if not re.search(r'[0-9!@#$%^&*()]', password):
            raise ValueError('Пароль должен содержать хотя бы одну цифру или специальный символ')

        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, simple_password: str, hashed_password: str) -> bool:
        """
            Checks passwords for identity
        :param simple_password: Unencrypted password
        :param hashed_password: Hashed password
        :return: bool
        """
        return bcrypt.checkpw(simple_password.encode('utf-8'), hashed_password.encode('utf-8'))

    @validates('password_hash')
    def validate_password_hash(self, key, password_hash: str) -> str | None:
        if len(password_hash) != 60:
            raise ValueError('Некорректный хеш пароля')
        return password_hash


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(Integer(), autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey('categories.id'), nullable=True)


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer(), autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(String(2048))
    price: Mapped[float]
    stock: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    seller_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False)


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(BigInteger(), autoincrement=True, primary_key=True)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.PENDING)
    total_amount: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    buyer_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    shipping_address_id: Mapped[Optional[int]] = mapped_column(ForeignKey('addresses.id'))


class OrderItem(Base):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    quantity: Mapped[int]
    price_at_purchase: Mapped[float]

    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)


class Address(Base):
    __tablename__ = 'addresses'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    street: Mapped[str] = mapped_column(String(256), nullable=False)
    city: Mapped[str] = mapped_column(String(64), nullable=False)
    state: Mapped[str] = mapped_column(String(64), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(32), nullable=False)
    country: Mapped[str] = mapped_column(String(64), nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)


class Payment(Base):
    __tablename__ = 'payments'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    amount: Mapped[float] = mapped_column(nullable=False)
    transaction_id: Mapped[str] = mapped_column(String(128), unique=True)
    payment_method: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), nullable=False)


class Review(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    rating: Mapped[int] = mapped_column(nullable=False)  # 1-5
    comment: Mapped[str] = mapped_column(String(1024))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)

    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='rating_range'),
    )


class Cart(Base):
    __tablename__ = 'carts'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)


class CartItem(Base):
    __tablename__ = 'cart_items'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    quantity: Mapped[int] = mapped_column(default=1, nullable=False)

    cart_id: Mapped[int] = mapped_column(ForeignKey('carts.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)


__all__ = ["User", "Category", "Product", "Order",
           "OrderItem", "Address", "Payment", "Review",
           "Cart", "CartItem", "PaymentStatus", "OrderStatus", "UserRole"]