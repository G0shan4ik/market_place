from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from .core import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)  # admin, seller, buyer
    orders: Mapped[str] = mapped_column(nullable=True)


class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[bool] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))


class Seller(Base):
    __tablename__ = "seller"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    inn: Mapped[str] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class Buyer(Base):
    __tablename__ = "buyer"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)


class SubCategory(Base):
    __tablename__ = 'subcategory'
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))


class Product(Base):
    __tablename__ = 'product'
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    article: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    subcategory_id: Mapped[int] = mapped_column(ForeignKey('subcategory.id'))
    seller_id: Mapped[int] = mapped_column(ForeignKey('seller.id'))