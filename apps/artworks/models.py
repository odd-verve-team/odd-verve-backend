from sqlalchemy import Column, String, Integer, Numeric, ForeignKey, Enum, DateTime, JSON, Table
from sqlalchemy.orm import relationship
import enum
import datetime

from config.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)


class ArtworkStatus(str, enum.Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    SOLD = "sold"

class Artwork(Base):
    __tablename__ = "artworks"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    price = Column(Numeric(10, 2), nullable=False)
    dimensions = Column(String)
    year = Column(Integer)
    technique = Column(String)
    images = Column(JSON, default=[])  # URLs із Cloudinary / S3
    status = Column(Enum(ArtworkStatus), default=ArtworkStatus.AVAILABLE)
    
    artist_id = Column(String, ForeignKey("users.id"))
    category_id = Column(String, ForeignKey("categories.id"))

    artist = relationship("User", back_populates="artworks")
    category = relationship("Category")