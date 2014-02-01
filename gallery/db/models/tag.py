from sqlalchemy import Column, Index, Integer, VARCHAR, Text

from gallery.db.models.base import Base

class Tag(Base):
    __tablename__ = 'tag'
    label = Column(VARCHAR(64), primary_key=True)

Index('tag_label', Tag.label, unique=True)
