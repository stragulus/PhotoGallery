from pyramid.config import Configurator
from gallery.db import init_db
from gallery import config

application = None

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    init_db(engine_settings = dict(pool_size = 5, max_overflow = 10))
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('imageserver', 'view/*args')
    config.scan()
    return config.make_wsgi_app()
