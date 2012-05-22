'''
SongScoop.py - Main functionality of the mp3 downloading program
               is contained in this file. The specific functionality 
               of parsing and downloading from individual sites is
               maintained in their respective modules. This module
               serves simply to be the glue holding those libraries 
               together, and allowing user input to the program.

@author: Jason Dsouza
'''

__author__ = ('jasonrdsouza (Jason Dsouza)')

import mp3skull
import sys
import getopt
import codecs
import csv
import urllib2
import shutil
import urlparse
import os


class Sites:
    '''Enum structure containing all the possible download locations'''
    MP3SKULL = 0


def str_to_site(str_arg):
    '''Helper function to convert a user input string into the proper
       Sites enum value'''
    if str_arg.lower() == 'mp3skull':
        return Sites.MP3SKULL
    else:
        return None


def choose_downloader(site):
    '''Choose which module (and thus site) will be used to do the
       downloading for this session'''
    if site == Sites.MP3SKULL:
        downloader = mp3skull
    else:
        downloader = None
    return downloader


def download_song(song, downloader):
    '''Function that does the main work of invoking the selected
       downloader, and taking all the steps necessary to download
       the desired song. Downloaders can easily be written and 
       integrated into this framework. They must simply follow the
       interface of .getSongLink(song). Consult existing
       downloaders for further clarification.'''
    if downloader == None:
        print 'Bad downloader'
        return
    song_url = downloader.getSongLink(song)
    web_download(song_url, song+'.mp3')
    print 'Finished downloading: {}'.format(song)


def web_download(url, fileName=None):
    '''Function to allow downloading of an mp3 file once the target
       URL is known. Tries to extract the filename from the HTTP
       response Content-Disposition, but if not, defaults to the
       url basename.'''
    def getFileName(url,openUrl):
        if 'Content-Disposition' in openUrl.info():
            # If the response has Content-Disposition, try to get filename from it
            cd = dict(map(
                lambda x: x.strip().split('=') if '=' in x else (x.strip(),''),
                openUrl.info()['Content-Disposition'].split(';')))
            if 'filename' in cd:
                filename = cd['filename'].strip("\"'")
                if filename: return filename
        # if no filename was found above, parse it out of the final URL.
        return os.path.basename(urlparse.urlsplit(openUrl.url)[2])

    r = urllib2.urlopen(urllib2.Request(url))
    try:
        fileName = fileName or getFileName(url,r)
        with open(fileName, 'wb') as f:
            shutil.copyfileobj(r,f)
    finally:
        r.close()


def usage():
    '''Prints usage information for the program, outlining what all
       the different command line flags do.'''
    print 'Command line options:'
    print '--song [name of song to download]'
    print '--site [name of download site to use]'
    print '--songfile [plaintext file with 1 song per line]'
    print '--help'


def main():
    '''Main method that handles user input'''
    # Parse command line options (if present)
    try:
        opts, args = getopt.getopt(sys.argv[1:], '', ['song=', 'site=', 'songfile=', 'help'])
    except getopt.error, msg:
        usage()
        print 'Error:', str(msg)
        sys.exit(2)
    # defaults
    song = None
    songfile = None
    site = Sites.MP3SKULL
    # process options
    for option, arg in opts:
        if option == '--song':
            song = arg
        elif option == '--site':
            site = str_to_site(arg)
        elif option == '--songfile':
            songfile = arg
        elif option == '--help':
            usage()
        else:
            print 'Unrecognized parameter... try --help'
    # react to user input
    downloader = choose_downloader(site)
    if song != None:
        download_song(song, downloader)
    if songfile != None:
        with open(songfile, 'r') as f:
            for line in f:
                line = line.strip('\n')
                download_song(line, downloader)
        assert f.closed


if __name__ == '__main__':
    main()

