from sqlalchemy import Column, Integer, String, DateTime
from database.base import Base
from sqlalchemy.sql import func


class AddressRequest(Base):
    __tablename__ = "address_requests"

    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)
    timestamp = Column(DateTime, server_default=func.now())
