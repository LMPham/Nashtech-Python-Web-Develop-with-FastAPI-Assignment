from sqlalchemy import Boolean, Column, ForeignKey, String, Uuid
from sqlalchemy.orm import relationship
from passlib.context import CryptContext

from database import Base
from entities.base_entity import BaseEntity

bcrypt_context = CryptContext(schemes=["bcrypt"])

class User(BaseEntity, Base):
    __tablename__ = "users"
    
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    company_id = Column(Uuid, ForeignKey("companies.id"), nullable=False)
    
    company = relationship("Company")
    tasks = relationship("Task", back_populates="user")


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)