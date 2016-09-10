#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
from datetime import *
import ConfigParser
from retrying import retry
import os
import sys

sys.path.append(r'C:\Users\David\Dropbox\djb_libraries')

from djb_email import sendEmail  # I haven't posted this module, so you'll have to use your own email code.
from posting_class import posting
from settings import *


# create min and max check time - allow some buffer in case the script takes too long
min_check_time = datetime.now() - timedelta(minutes=(script_frequency+15))
max_check_time = datetime.now() - timedelta(minutes=7)


# read config file
config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'locations.config')
locations_config = ConfigParser.ConfigParser()
locations_config.read(config_path)


### functions

def getCraigslistPage():
    """ make request to page """
    global url_part  # being lazy...
    if len(url_part) > 0:
        url_part = url_part+'/'        
    
    base_url = 'http://'+craigslist_subdomain+'.craigslist.ca/search/'+url_part+'apa?sort=date'+'&max_price='+str(max_price)+'&min_price='+str(min_price)

    @retry(wait_fixed=2000, stop_max_attempt_number=5)
    def make_request(base_url):
        r = requests.get(base_url)
        return r

    r = make_request(base_url)
    page_source = r.text
    soup = BeautifulSoup(page_source, 'html.parser')
    return soup



def makeListOfPostings(soup):
    """ create a list of posting objects """
    content = soup.findAll("div", { "class" : "content" })
    soup = BeautifulSoup(str(content), 'html.parser')
    posting_list = soup.find_all('p')
    return posting_list



def lookForNewPostings(posting_list):
    """ return list of postings that have been posted since the last time the script ran """
    new_apartment_list = []
    for apartment_posting in posting_list:
        try:
            post = posting(apartment_posting)
            if (post.posting_time >= min_check_time) and (post.posting_time <= max_check_time):
                new_apartment_list.append(post)
            else:
                break
        except Exception as e:
           print 'error getting posting_time: '+str(sys.exc_type)+' '+str(e)

    return new_apartment_list



def checkPostingLocations(new_apartment_list):
    """ 
        - check a list of apartment posting objects to see if their lattitude and longitude matches the defined areas
        - returns a list of strings with the title of the apartment and the link to the apartment posting
    """
    in_range_apartments = []   
    
    for apartment_posting in new_apartment_list:
        try:
            apartment_posting.get_lat_and_long()
            for area_name in locations_config._sections.iterkeys():
                if (
                        apartment_posting.lat > float(locations_config._sections[area_name]['min_lat'])
                        and apartment_posting.lat < float(locations_config._sections[area_name]['max_lat'])
                        and apartment_posting.long > float(locations_config._sections[area_name]['min_long'])
                        and apartment_posting.long < float(locations_config._sections[area_name]['max_long'])
                    ):
                    
                    in_range_apartments.append(str(area_name)+': '+str(apartment_posting.title.string))
                    in_range_apartments.append(str(apartment_posting.link))
                                        
                    break
        
        # except if there's an error getting the latitude and longitude:
        except Exception as e:
            print 'error getting post: '+str(sys.exc_type)+': '+str(e)

    return in_range_apartments



def sendApartmentEmail(in_range_apartments):
    """ send apartment email """
    subject = 'Apartments Found In Area'
    se = sendEmail()
    se.html(subject, 'djb.reports@gmail.com', to_email, in_range_apartments)
    return




# search craigslist and send the emails:
if __name__ == "__main__":

    print "starting "+str(datetime.now())

    html = getCraigslistPage()

    posting_list = makeListOfPostings(html)

    new_postings = lookForNewPostings(posting_list)

    if len(new_postings) == 0:
        print 'no new apartments: '+str(datetime.now())
        sys.exit()
    else:
        in_range_apartments = checkPostingLocations(new_postings)

        if len(in_range_apartments) == 0:
            print 'no new apartments: '+str(datetime.now())
            sys.exit()

        else:
            # I havent posted this email module yet, so you'll have to write your own code for that. Sorry!
            sendApartmentEmail(in_range_apartments)
            print 'In Area email sent: '+str(datetime.now())
         

