import requests
from bs4 import BeautifulSoup
from datetime import *
import sys

class posting:
    def __init__(self, bs4_object):
    
        # id
        try:
            self.id = bs4_object['data-pid']
        except Exception as e:
            print 'no id: '+str(sys.exc_type)+' '+str(e)
            self.id = None
        
        # posting_time
        try:
            posting = bs4_object.span.find_all("span", { "class" : "pl" })
            soup = BeautifulSoup(str(posting), 'html.parser')
            self.posting_time = datetime.strptime(soup.time['datetime'], '%Y-%m-%d %H:%M')
        except Exception as e:
            print 'no posting_time: '+str(sys.exc_type)+' '+str(e)
            self.posting_time = None
        
        # link
        try:
            self.link = 'http://vancouver.craigslist.ca/'+bs4_object.a['href']
        except Exception as e:
            print 'no link: '+str(sys.exc_type)+' '+str(e)
            self.link = None
        
        # title
        try:
            self.title = bs4_object.span.find("a", { "class" : "hdrlnk" }).contents[0]
        except Exception as e:
            print 'no title: '+str(sys.exc_type)+' '+str(e)
            self.title = None
        
        # area_description
        try:
            self.location_description = bs4_object.find("span", { "class" : "pnr" }).small.contents[0].replace('(','').replace(')','')
        except Exception as e:
            print 'no area_description: '+str(sys.exc_type)+' '+str(e)
            self.location_description = None
        
    def get_lat_and_long(self):
        r = requests.get(self.link)
        soup = BeautifulSoup(r.text, 'html.parser')

        map_div = soup.findAll("div", { "class" : "viewposting", "id" : "map" })

        self.lat = float(map_div[0]['data-latitude'])
        self.long = float(map_div[0]['data-longitude'])

    def get_posting_body(self):
        r = requests.get(self.link)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        posting_body = soup.findAll("section", { "id" : "postingbody" })
        
        self.posting_body = str(posting_body[0].contents)
        
        
