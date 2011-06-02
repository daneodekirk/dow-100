import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from google.appengine.dist import use_library
use_library('django', '1.2')

import time
import math
import logging
from datetime import datetime

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from django.utils import simplejson

from resources.median import Median 
from resources.mean import Mean
import resources.graphs as graph

from mpmath import *

class MainPage(webapp.RequestHandler):
    def get(self):
        descriptions = graph.types

        template_values = {
          'graphs' : descriptions
        }
        path = os.path.join(os.path.dirname(__file__),
            'index.html')
        self.response.out.write(template.render(path,
            template_values))

class JSONHandler(webapp.RequestHandler):
    """ Will handle the JSON requests."""
    def __init__(self):
        webapp.RequestHandler.__init__(self)
        self.methods = JSONMethods()
        
    def get(self):
        func = None
        action = self.request.get('graph')
        if action:
            if action[0] == '_':
                self.error(403) # access denied
                return
            else:
                func = getattr(self.methods, action, None)

        if not func:
            self.error(404) # file not found
            return

        args = ()
        kwargs = {}
        key = ['sample', 'degree']
        for key in key:
            val = self.request.get(key)
            if key == 'sample':
                if not val:
                    val = 60
                else:
                    val = int(val)
            if key == 'degree':
                if not val:
                    val = 3
                else:
                    val = int(val)

            kwargs[key] = val

        t = time.time()
        result = func(**kwargs)
        result['time'] = time.time() - t
        self.response.out.write(simplejson.dumps(result))
        

class JSONMethods:
    """ Defines the methods that can be JSONed.
    NOTE: Do not allow remote callers access to private/protected "_*" methods.
    """
    def __init__(self, *args, **kwargs):
        self.sample = 60
        self.data = self.__parse(self.sample)
    
    def basic(self, sample=60, **kwargs):
        data = self.__parse(sample)
        return {'points': data}
        
    def fourier(self, *args):
        pass

    def medians(self, sample=60, **kwargs):
        data = self.__parse(sample)
        logging.debug('Medians: length of sample data is %d' % len(data))
        median = Median(data, 3).median()
        return {'points': median}
        
    def means(self, sample=60, **kwargs):
        data = self.__parse(sample)
        logging.debug('Means: length of sample data is %d' % len(data))
        mean = Mean(data).mean()
        return {'points': mean }

    def chebyshev(self, sample=60, *args, **kwargs):
        #[TODO] this needs work
        data = self.__parse(sample)
        endpoints = [0,len(self.data)-1]
        mp.dps = 15; mp.pretty = True
        poly, err = chebyfit(self.test, endpoints, 15, error=True)

        end = float(data[-1][1])
        step = end/len(data)

        for i in range(len(data)):
            logging.debug((i*step))

                
        points = [[nstr(polyval(poly, i*step)), i*step] for i in range(len(data))
                        if i*step < end]

        return {'points': points}

    def test(self,x):
        x = int(x)
        y = [float(point[1]) for point in self.data]
        return y[x]
  
    def f(self, x):
        x = int(x)
        return float(self.data[x][1])

    def __parse(self, sample=60):
        """ Parses the dow jones text file into a list """
        f  = open('dj-100.txt', 'r')
        dj = [line.rstrip().split(',') for line in f]
        dj = [dj[i] for i in range(len(dj)) 
                        if i % sample == 0 and 0 < i < len(dj)]
        return self.__normalize(dj)

    def __normalize(self, dj):
        """ Normalized the year in the data to retrun 
            a unix timestamp for even pre-1970 years.
            Also handles the Y2K issue.
        """
        epoch = datetime(1970, 1, 1)
        cache = 1900
        prefix = '19' 
        ndj = []
        for date in dj:
            l = prefix+date[0]
            if int(l[:4]) < cache:
                prefix = '20'
                l = prefix+date[0]
            cache = int(l[:4])
            d = datetime(int(l[:4]), int(l[4:6]), int(l[6:8]))
            diff = d-epoch
            t = diff.days * 24 * 3600 + diff.seconds
            ndj.append([t*1000, date[1]])
        return ndj

class AboutPage(webapp.RequestHandler):
    def get(self):
        template_values = {
          'title' : 'About This App'
        }
        path = os.path.join(os.path.dirname(__file__),
            'about.html')
        self.response.out.write(template.render(path,
            template_values))

    


application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/json', JSONHandler),
                                      ('/about', AboutPage),
                                     ], debug=True)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
