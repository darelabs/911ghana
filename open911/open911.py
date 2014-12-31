import webapp2
from google.appengine.ext import ndb

import pages
import PyGeoRSS
import datetime
from cStringIO import StringIO
from geopy.geocoders import Nominatim




DEFAULT_OPEN911_NAME = 'test'

# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

def open911_key(open911_name=DEFAULT_OPEN911_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('Open911_name', open911_name)


class Emergency(ndb.Model):
    location_name = ndb.StringProperty()
    geoloc = ndb.GeoPtProperty()
    complaint = ndb.StringProperty()
    # complainant = ndb.StringProperty() 
    timestamp = ndb.DateTimeProperty(auto_now_add=True)




class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        # self.response.write('Hello, World!')
        self.response.write( pages.index % {'msg':''} )



    def post(self):
        #Simply post data into datastore.
        #and confirm post

        open911_name = self.request.get('open911_name',
                                          DEFAULT_OPEN911_NAME)
        
        lat, lng = self.request.get('location', '(0,0)')[1:-1].split(",")
        geolocator = Nominatim()
        location = geolocator.reverse(self.request.get('location', '(0,0)')[1:-1])

        call = Emergency( geoloc=ndb.GeoPt(lat, lng) )
        call.complaint = self.request.get('complaint')
        call.location_name = location.address
        
        try:
            call.put()
            self.response.write( pages.index % context )
        except:
            self.response.write( pages.index % {'msg':'System error.'} )





class RssCrime(webapp2.RequestHandler):
    def get(self):
        # Ancestor Queries, as shown here, are strongly consistent with the High
        # Replication Datastore. Queries that span entity groups are eventually
        # consistent. If we omitted the ancestor from this query there would be
        # a slight chance that Greeting that had just been written would not
        # show up in a query.
        # open911_query = Emergency.query(
        #     ancestor=open911_key(open911_name)).order(-Emergency.timestamp)
        # emergencies = open911_query.fetch(15)

        qry = Emergency.query().order(-Emergency.timestamp)
        emergencies = qry.fetch(15)


        list_of_reported_crimes = []
        i = 0

        for crime in emergencies:
            i += 1
            list_of_reported_crimes.append(
            PyGeoRSS.RSSItem(
                title = "#gh911_test",
                link = "http://siteopen911.appspot.com/",
                description = crime.complaint,
                pubDate = crime.timestamp,
                guid = PyGeoRSS.Guid("http://siteopen911.appspot.com/%s" % str(i) ),
                geo_rss_pt = PyGeoRSS.GeoRssPoint(crime.geoloc.lat, crime.geoloc.lon),
                #location = PyGeoRSS.GeoRssPoint(0, 0),
                )
            )
            

        rss = PyGeoRSS.RSS2(
            title = "911Ghana Crime feed",
            link = "http://siteopen911.appspot.com/rsscrime",
            description = "Realtime crime feed.",
            lastBuildDate = datetime.datetime.now(),

            items = list_of_reported_crimes)

        rss_response = StringIO()
        rss.write_xml(rss_response)
        d = datetime.datetime.now()

        self.response.headers["Content-Type"] = "application/rss+xml"
        self.response.headers.add_header("Expires", d.strftime("%a, %d %b %Y %H:%M:%S GMT"))
        self.response.write(rss.to_xml())

        rss_response.close()
        



application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/rsscrime.*', RssCrime),
], debug=True)
