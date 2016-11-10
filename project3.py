## Project: Project 3
## Class: CSI-382: NLP
## Creator: Emily Johnson
## Date Created: November 5, 2015
## Date Edited:  November 10, 2016
## Description: Originally created for CSI-210: Software Engineering for the
##              Pick A Flick Project, but was then repurposed for CSI-382: NLP.
##         NOW: It goes through the Muhlenberg website and stores the HTML,
##              while adding the links to other websites to a stack that will be
##              added later.
##  IT USED TO: scrape IMDb and adds values to a database.

import re       # Imports RegEx
import urllib # Imports the ability to download files from URLs
import urllib2 # Ability to use URLS
import requests # Requests allow HTTP/1.1 requests
from BeautifulSoup import BeautifulSoup # Import ability to scrape websites BeautifulSoup3

# Setting the null value
NULL = None

# Gets the movies and tags, then commits whatever changes have been made
def main():
    getLinks()

# Finds all of the links in a webpage (currently muhlenberg.edu) and stores them
# in a queue.
def getLinks():
    url = 'http://www.muhlenberg.edu/'
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)

    for ultag in soup.findAll('ul'):
        for litag in ultag.findAll('li'):
            # Gets the information of each movies that is most easily accessible on the
            # list of movies.
            if (litag.a != None):
                title = litag.a.text
                title = title.replace("'", "''");

                # Gets the new URL for each movie.
                newLink = (litag.a.get('href'))
                if(re.match(r"http\:\/\/", newLink[0:7])):
                    print newLink
                else:
                    newLink = "http://www.muhlenberg.edu" + newLink
                    print newLink

            print "SAVE ME PLEASE!!"





main()          # Calls the main function
