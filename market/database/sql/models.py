from sqlalchemy import ForeignKey, Text, Integer, BigInteger, Float, Boolean
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from .core import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger(), autoincrement=True, primary_key=True, unique=True)
    email: Mapped[str] = mapped_column(Text(), nullable=False)
    phone_number: Mapped[str] = mapped_column(Text(), nullable=False)
    password: Mapped[str] = mapped_column(Text(), nullable=False)
    orders: Mapped[str] = mapped_column(Text(), nullable=True)

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))


class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(BigInteger(), autoincrement=True, primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer())
    status: Mapped[bool] = mapped_column(Boolean())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))


class Seller(Base):
    __tablename__ = "seller"

    id: Mapped[int] = mapped_column(BigInteger(), autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(Text())
    inn: Mapped[str] = mapped_column(Text())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


# class Buyer(Base):
#     __tablename__ = "buyer"
#
#     id: Mapped[int] = mapped_column(BigInteger(), autoincrement=True, primary_key=True)
#     name: Mapped[str] = mapped_column(Text())
#
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(BigInteger(), autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(Text())


class SubCategory(Base):
    __tablename__ = 'subcategory'
    id: Mapped[int] = mapped_column(BigInteger(), autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(Text())

    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))


class Product(Base):
    __tablename__ = 'product'
    id: Mapped[int] = mapped_column(BigInteger(), autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(Text())
    price: Mapped[float] = mapped_column(Float())
    article: Mapped[str] = mapped_column(Text())
    description: Mapped[str] = mapped_column(Text())

    subcategory_id: Mapped[int] = mapped_column(ForeignKey('subcategory.id'))
    seller_id: Mapped[int] = mapped_column(ForeignKey('seller.id'))


__all__ = ["Users", "Orders", "Category", "SubCategory",
           "Product", "Seller"]