from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from gallery.db import session
from gallery.db.models.base import Base

application = None

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    global application
    engine = engine_from_config(settings, 'sqlalchemy.')
    session.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.scan()
    application = config.make_wsgi_app()
    return application
