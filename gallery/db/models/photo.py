import random
import string

from sqlalchemy import CHAR, Column, Index, Integer, VARCHAR, Table, Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from gallery.db import session
from gallery.db.models.base import Base
from gallery.db.models.photo_tag import PhotoTag
from gallery.db.models.tag import Tag

class Photo(Base):
    __tablename__ = 'photo'

    id = Column(Integer, primary_key=True)
    key = Column(CHAR(16), unique=True, nullable=False)
    path = Column(Text, nullable=False)

    tags = relationship("Tag", secondary=PhotoTag.__table__, backref="photos")

    def __init__(self, path):
        self.key = ''.join(random.choice(string.letters + string.digits) for x in range(16))
        self.path = path

    def set_tags(self, tag_labels):
        from gallery.db.models import Tag
        tags = []

        for label in tag_labels:
            t = session.query(Tag).filter(Tag.label == label).first()
            if not t:
                t = Tag(label)
                session.add(t)
            
            tags += [ t ]

        self.tags = tags
        session.flush()

    def get_link(self, width=None):
        return '/view/%s%s' % (self.key, '/%d' % width if width != None else '')

    @staticmethod
    def find_by_tag(txt):
        #.join(PhotoTag,Tag)\
        q = session.query(Photo)\
            .join(Photo.tags)\
            .filter(Tag.label.like('%' + txt + '%'))
        return q

            

Index('photo_key', Photo.key, unique=True)
