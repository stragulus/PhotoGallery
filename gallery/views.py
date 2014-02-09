from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from gallery.db import session
from gallery.db.models import Photo, PhotoTag, Tag


@view_config(route_name='home', renderer='templates/gallery.pt')
def my_view(request):
    if 'q' in request.params:
        q = request.params['q']
        pictures = session.query(Photo)\
            .join(Photo.tags)\
            .filter(Tag.label.like('%%%s%%' % q))
            .all()
    else:
        pictures = []
    #return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {
        'pictures': pictures
    }
