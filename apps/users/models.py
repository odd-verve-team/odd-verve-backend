from sqlalchemy import Column, String, Integer, Numeric, ForeignKey, Enum, DateTime, JSON, Table
from sqlalchemy.orm import declarative_base, relationship
import enum
import datetime

from config.database import Base

class UserRole(str, enum.Enum):
    CUSTOMER = "customer"
    ARTIST = "artist"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True) # UUID
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER)
    avatar_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    artworks = relationship("Artwork", back_populates="artist")
