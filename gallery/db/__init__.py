from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

from gallery import config
from gallery.db.models.base import Base

_session = None

def init_db(db_uri=None, engine_settings=None, session_settings=None):

    if not db_uri:
        db_uri = config.db_uri

    default_engine_settings = dict(
        pool_size = 1,
        max_overflow = 5,
        pool_recycle = 180
    )
    if engine_settings:
        default_engine_settings.update(engine_settings)

    engine = create_engine(db_uri, **default_engine_settings)
        
    # autocommit: If True, don't always start a transaction
    #             for each session, start one manually
    # autoflush:  Only explicitly flush data to the database
    default_session_settings = dict(
        autocommit = True,
        autoflush = False,
        expire_on_commit = False,
    )
    if session_settings:
        default_session_settings.update(session_settings)

    session_maker = sessionmaker()
    session_maker.configure(bind=engine, **default_session_settings)
    global _session
    # thread-local sessions!
    _session = scoped_session(session_maker)
    Base.metadata.bind = engine

class SessionWrapper(object):
    def __getattribute__(self, name):
        global _session
        return _session.__getattribute__(name)
        
# wrap the session such that when code imports session before init_db is called,
# it will still work.
session = SessionWrapper()
__all__ = [ 'session', 'init_db' ]
