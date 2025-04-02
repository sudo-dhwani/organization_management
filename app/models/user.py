from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.models.base import Base  # Ensure this file exists

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    role = Column(String(50), default="user")  # "admin" or "user"
    created_at = Column(DateTime, server_default=func.now())

    # Relationship with organization
    organization = relationship("Organization", back_populates="users")
