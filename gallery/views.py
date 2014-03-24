import Image
import os

from pyramid import httpexceptions
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
            .filter(Tag.label.like('%%%s%%' % q)) \
            .all()
    else:
        pictures = []
    #return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {
        'pictures': pictures
    }

@view_config(route_name='imageserver')
def image_server(request):
    if not 'key' in request.params:
        return httpexceptions.HTTPBadRequest('Missing key parameter')

    p = session.query(Photo).filter_by(key = request.params['key']).first()
    if not p:
        return httpexceptions.HTTPNotFound('Could not find that image')

    path = p.path

    if not os.path.exists(path):
        return httpexceptions.HTTPNotFound('Da plaatje ken ik nie vinde nie')

    scale = request.params.get('scale')
    if scale != None:
        try:
            scale = int(scale)
        except ValueError:
            return httpexceptions.HTTPBadRequest('Invalid scale parameter')

        if scale < 16 or scale > 1024:
            return httpexceptions.HTTPBadRequest("Scale value outside acceptable range")
        
        from StringIO import StringIO
        img = Image.open(path)
        b = StringIO()
        img.thumbnail((scale, scale), Image.ANTIALIAS)
        img.save(b, "JPEG")
        b.seek(0)
        pdata = b.read()
    else:
        pdata = open(p.path).read()

    # hardcoded jpg for now
    return Response(body=pdata, content_type='image/jpeg')
