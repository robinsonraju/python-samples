import os
import re
import sys
import urllib2
from xml.dom import minidom

from string import letters

import webapp2
import jinja2
import logging

from google.appengine.ext import db
from google.appengine.api import memcache

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

art_key = db.Key.from_path('ASCIIChan', 'arts')

def console(s):
    sys.stderr.write('%s\n' % s)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
            self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
            t = jinja_env.get_template(template)
            return t.render(params)

    def render(self, template, **kw):
            self.write(self.render_str(template, **kw))

GMAPS_URL = "http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false&"
def gmap_img(points):
    markers = '&'.join('markers=%s,%s' % (p.lat, p.lon) for p in points)
    return GMAPS_URL + markers

IP_URL = "http://api.hostip.info/?ip="
def get_coords(ip):
    url = IP_URL + ip
    content = None
    try:
        content = urllib2.urlopen(url).read()
    except URLError:
        return

    if content:
        d = minidom.parseString(content)
        coords = d.getElementsByTagName("gml:coordinates")
        if coords and coords[0].childNodes[0].nodeValue:
            lon, lat = coords[0].childNodes[0].nodeValue.split(',')
            return db.GeoPt(lat, lon)

class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    coords = db.GeoPtProperty( )


def top_arts(update = False):
    key = 'top'
    arts = memcache.get(key)
    if arts is None or update:
        logging.error("DB QUERY")
        arts = db.GqlQuery("SELECT * "
                                    "FROM Art "
                                    "WHERE ANCESTOR IS :1 "
                                    "ORDER BY created DESC "
                                    "LIMIT 10",
                                    art_key)
        arts = list(arts)
        memcache.set(key, arts)
    return arts

class AsciiChanHandler(Handler):
    def render_front(self, title="", art="", error=""):
        arts = top_arts()

        #find which arts have coords
        img_url = None
        points = filter(None, (a.coords for a in arts))
        if points:
                img_url = gmap_img(points)

        self.render("ascii_chan.html", title = title, art = art, error = error, arts = arts, img_url = img_url)

    def get(self):
        #self.write(repr(get_coords(self.request.remote_addr)))
        self.render_front()

    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")

        if title and art:
            p = Art(parent=art_key, title = title, art = art)
            #lookup the user's coordinates from their IP
            coords = get_coords(self.request.remote_addr)
            #if we have coordinates, add them to the art
            if coords:
                    p.coords = coords

            p.put()
            #rerun the query and update the cache
            top_arts(True)

            self.redirect("/cs253/unit5/asciichan")
        else:
            error = "we need both a title and some artwork!"
            self.render_front(error = error, title = title, art =art)
