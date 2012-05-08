'''
Created on Sep 5, 2011

@author: Guga
'''
import re
import operator

import urllib2
from BeautifulSoup import BeautifulSoup # html parser


Unfetched_URLs = []

def fetchWebpage(url):
    '''Helper function that takes a URL and returns a file object
       whose contents are the html contents of the webpage'''
    try: 
        f = urllib2.urlopen(url)
        return f
    except urllib2.HTTPError, e:
        print 'Could not fetch: {}'.format(url)
        Unfetched_URLs.append(url)
        return None
    except urllib2.URLError, e:
        print 'Could not fetch: {}'.format(url)
        Unfetched_URLs.append(url)
        return None

def getSongLink(song, link_num=0):
    '''Function to return a link to the given song on MP3Skull'''
    url_keyword = song.replace(' ', '_')
    url = 'http://mp3skull.com/mp3/{}.html'.format(url_keyword)
    # get html page for song
    f = fetchWebpage(url)
    soup = BeautifulSoup(f.read())
    linkList = soup('a', {'rel':'nofollow', 'target':'_blank', 'style':'color:green;'})
    return linkList[link_num].attrMap['href']
    
