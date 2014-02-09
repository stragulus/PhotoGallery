from sqlalchemy import CHAR, Column, Index, Integer, VARCHAR, Table, Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from gallery.db.models.base import Base

class PhotoTag(Base):
    __tablename__ = "photo_tag"
    photo_id = Column(Integer, ForeignKey('photo.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tag.id'), primary_key=True)


