import urllib   # Imports the ability to download files from URLs
import urllib2  # Ability to use URLS
from urllib2 import HTTPError, URLError
import requests # Requests allow HTTP/1.1 requests
import cPickle as pickle
from BeautifulSoup import BeautifulSoup # Import ability to scrape websites BeautifulSoup3
from socket import timeout


def main():
    visitedHash = dict()
    with open('Files/visitedLinks.p', 'rb') as handle:
        visitedHash = pickle.load(handle)
    swapDict = dict((v,k) for k,v in visitedHash.iteritems())
    print "You are missing files:"
    for i in range(1, 10001):
        try:
            tempDoc = open("Files/Documents/doc" + str(i) +".txt", 'r')
            tempDoc.close()
        except:
            url = swapDict.get(i, False)
            try:
                html = urllib.urlopen(url).read()
                # html = urllib2.urlopen(url, timeout = 10).read()
            except:
                print "Still need to make doc" + str(i)
                continue
            # except (HTTPError, URLError) as error:
            #     print 'Delete doc %s, it was not retrieved because %s\tURL: %s', str(i), error, url
            #     continue
            # except timeout:
            #     print 'Delete doc %s, it was not retrieved because socket timed out - URL %s', str(i), url
            #     continue
            else:
                print "doc" + str(i)
                soup = BeautifulSoup(html)
                writeDoc = open("Files/Documents/doc" + str(i) +".txt", 'w')
                for line in soup.prettify():
                    writeDoc.write(line)
                writeDoc.close()



main()
