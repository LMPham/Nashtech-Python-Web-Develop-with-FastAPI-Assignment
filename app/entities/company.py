import enum

from sqlalchemy import Column, Enum, SmallInteger, String
from sqlalchemy.orm import relationship

from database import Base
from entities.base_entity import BaseEntity
from entities.user import User

class CompanyMode(enum.Enum):
    PENDING = "PENDING"
    STARTUP = "STARTUP"
    ESTABLISHED = "ESTABLISHED"
    CLOSED = "CLOSED"

class Company(BaseEntity, Base):
    __tablename__ = "companies"
    
    name = Column(String)
    description = Column(String)
    mode = Column(Enum(CompanyMode), default=CompanyMode.PENDING)
    rating = Column(SmallInteger, default=0)
    
    users = relationship("User", back_populates="company")