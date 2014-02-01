from sqlalchemy import CHAR, Column, Index, Integer, VARCHAR, Text

from gallery.db.models.base import Base

class Photo(Base):
    __tablename__ = 'photo'

    id = Column(Integer, primary_key=True)
    key = Column(CHAR(16), unique=True, nullable=False)
    path = Column(Text, nullable=False)

Index('photo_key', Photo.key, unique=True)
