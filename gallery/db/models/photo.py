import random
import string

from sqlalchemy import CHAR, Column, Index, Integer, VARCHAR, Table, Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from gallery.db.models.base import Base

photo_tag_table = Table('photo_tag', Base.metadata,
    Column('photo_id', Integer, ForeignKey('photo.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)

class Photo(Base):
    __tablename__ = 'photo'

    id = Column(Integer, primary_key=True)
    key = Column(CHAR(16), unique=True, nullable=False)
    path = Column(Text, nullable=False)

    tags = relationship("Tag", secondary=photo_tag_table, backref="photos")

    def __init__(self):
        self.key = ''.join(random.choice(string.letters + string.digits) for x in range(16))

Index('photo_key', Photo.key, unique=True)
