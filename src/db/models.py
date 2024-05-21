from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, name='id')
    stocks = Column(String, index=True, name='stocks')
    quantity = Column(Float, name='quantity')
    status = Column(String, default="pending")
