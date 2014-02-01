from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

# XXX set autocommit/transactional params here
session = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

__all__ = [ 'session' ]
