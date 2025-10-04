"""
User model for authentication and authorization
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Profile information
    phone = Column(String(20), nullable=True)
    department = Column(String(100), nullable=True)
    position = Column(String(100), nullable=True)
    bio = Column(Text, nullable=True)
    
    # Relationships
    documents = relationship("Document", back_populates="owner")
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"