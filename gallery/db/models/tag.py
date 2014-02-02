from sqlalchemy import Column, Index, Integer, VARCHAR, Text

from gallery.db.models.base import Base

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    label = Column(VARCHAR(64), unique=True)

# XXX isn't this duplicate?
Index('tag_label', Tag.label, unique=True)
