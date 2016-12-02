## Project: Project 3 try number 2
## Class: CSI-382: NLP
## Creator: Emily Johnson & Casie Ropski
## AIC: Jalal directed us to the solution of the problem with our files not
## being overwritten.

import re       # Imports RegEx
import urllib   # Imports the ability to download files from URLs
import urllib2  # Ability to use URLS
import requests # Requests allow HTTP/1.1 requests
import time     # Import time so that the crawler can be delayed to be polite
import cPickle as pickle
# try:
#    import cPickle as pickle
# except:
#    import pickle
import pprint
from StringIO import StringIO
from nltk.corpus import wordnet #For word stemming
from nltk.stem import WordNetLemmatizer #For word stemming
from BeautifulSoup import BeautifulSoup # Import ability to scrape websites BeautifulSoup3

## TODO:
##       - Modify beenThereDoneThat.txt to include /robots.txt
## TEST:
##       - Write to your file every time:
##          ~ Unsucessful opening the web page.
##          ~ Stack is empty.
##          ~ Write to your file every x documents.
## DONE:
##       - Make all of the words lowercase
##       - Add booleans to turn stops and stemming on and off.
##       - Delay the crawler so our IP address doesn't get banned.
##       - Adding another data stucture/file that stores the number of docs a
##         word appears in, as well as which documents the word appears in.
##          ~ Deal when there are already values in the casietokenByDocFreq.txt

# Setting the null value
NULL = None

# Global hash of stop words.
stopWords = dict()

# try:
#     # File to maybe use?
#     tokenDocID = open("Files/tokenByDocID.txt", 'r+')
# except:
#     tokenDocID = open("Files/tokenByDocID.txt", 'w')
#     tokenDocID.close()
#     tokenDocID = open("Files/tokenByDocID.txt", 'r+')

# try:
#     # Open up the global token file.
#     tokenDocFreq = open("Files/tokenByDocFreq.txt", 'r+')
# except:
#     tokenDocFreq = open("Files/tokenByDocFreq.txt", 'w')
#     tokenDocFreq.close()
#     tokenDocFreq = open("Files/tokenByDocFreq.txt", 'r+')

# Global hash of tokens with the doc's and frequency in each doc as the value
JuLiDoTheThing = dict()

# Global hash of tokens with their total count
GlobalDictForWordFreq = dict()

# Global hash of visited sites.
visitedHash = dict()

# Global hash of sites to avoid.
evadeAndConquor = dict()

# try:
#     # Open up the global visited sites file.
#     visitedLinks = open("Files/beenThereDoneThat.txt", 'r+')
# except:
#     visitedLinks = open("Files/beenThereDoneThat.txt", 'w')
#     visitedLinks.close()
#     visitedLinks = open("Files/beenThereDoneThat.txt", 'r+')

try:
    # Open the global links queue file.
    linksQueue = open("Files/linksQueue.txt", 'r+')
except:
    linksQueue = open("Files/linksQueue.txt", 'w')
    linksQueue.close()
    linksQueue = open("Files/linksQueue.txt", 'r+')



# Our instance of stemmer.
stemmer = WordNetLemmatizer()

# Boolean switches to turn off stop words, stemming words, and delay.
removeStopWords = True
stemWords = True
delay = False


def slowDown():
    time.sleep(5)

# Calls getLinks for the first time from whatever the root URL is
# (currently muhlenberg.edu)
def main():
    global j
    global visitedHash
    global JuLiDoTheThing
    global GlobalDictForWordFreq
    j = 0
    url = 'http://www.muhlenberg.edu/'
    linksQ.enqueue(url)

    limit = 5
    i = 0

    stopIntheNameofWords = open("stopwords.txt", 'r')
    for word in stopIntheNameofWords:
        word = str(word)
        stopWords[word.strip()] = stopWords.get(word.strip(), 0) + 1
    stopIntheNameofWords.close()

    robots = open("robot.txt", 'r')
    for word in robots:
        word = str(word)
        if re.search("Disallow", word):
            word = word[11:]
            word = word[:-2]
            # print word
            evadeAndConquor[word.strip()] = evadeAndConquor.get(word.strip(), 0) + 1
    robots.close()

    # Go through the file and convert each line to a key and value pair, with
    # the key being the url and the value being it's document number.
    try:
        # visitedHash = pickle.load( open( "Files/visitedLinks.p", "rb" ) )
        with open('Files/visitedLinks.p', 'rb') as handle:
            visitedHash = pickle.load(handle)
        j = len(visitedHash)
    except:
        print "File is empty."
    # for line in visitedLinks:
    #     line = str(line)
    #     line = line.strip()
    #     line = line.split(", ")
    #     # print line
    #     j+=1
    #     visitedHash[line[0]] = line[1]


    for line in linksQueue:
        line = str(line)
        line = line.strip()
        linksQ.enqueue(line)


    try:
        # GlobalDictForWordFreq = pickle.load( open( "Files/tokenDocID.p", "rb" ) )
        with open( "Files/tokenDocID.p", "rb" ) as handle:
            GlobalDictForWordFreq = pickle.load(handle)
    except:
        print "File is empty."
    # for line in tokenDocID:
    #     line = str(line)
    #     line = line.strip()
    #     line = line.split(", ")
    #     # print line
    #     try:
    #         GlobalDictForWordFreq[line[0]] = line[1]
    #     except:
    #         print "You made this one wrong:", line

    ## Uses pickle to populate the document frequency dictionary with the
    ## tokenDocFreq.p file.
    try:
        # JuLiDoTheThing = pickle.load( open( "Files/tokenDocFreq.p", "rb" ) )
        with open( "Files/tokenDocFreq.p", "rb" ) as handle:
            JuLiDoTheThing = pickle.load(handle)
    except:
        print "File is empty."

    ## This is not pretty, but it does successfully convert this string file into a
    ## int list data structure.

    # for line in tokenDocFreq:
    #     tempList = list()
    #     line = str(line)
    #     line = line.strip()
    #     line = line.split(", ", 1)
    #     try:
    #         # print line
    #         line[1] = line[1][2:len(line[1])-2]
    #         # print line[1]
    #         tempList = line[1].split("], [")
    #         # print tempList
    #         tempList2 = list()
    #         for item in tempList:
    #             item = item.split(", ")
    #             tempList2.append([int(item[0]), int(item[1])])
    #         JuLiDoTheThing[line[0]] = tempList2
    #     except:
    #         print "You made this one wrong:", line
    # for key, value in JuLiDoTheThing.items():
    #     print key, value


    #Get the links for the next document ????
    getLinks(i, limit+j)

    newLine = '\n'
    # visitedLinks.seek(0)
    # print visitedHash.items()
    # pickle.dump( visitedHash, open( "visitedLinks.p", "wb" ) )
    # emptyFile = open("Files/visitedLinks.p", 'w')
    # emptyFile.close()
    with open('Files/visitedLinks.p', 'wb') as handle:
        pickle.dump(visitedHash, handle)
    # data_string = pickle.dumps(visitedHash)
    # visitedLinks.write(data_string)
    # for key,value in visitedHash.items():
    #     tempString = str(key) + ", " + str(value)
    #     visitedLinks.write(tempString.strip())
    #     visitedLinks.write(newLine)

    # tempString = ""
    # tokenDocID.seek(0)
    # print GlobalDictForWordFreq.items()
    # pickle.dump( GlobalDictForWordFreq, open( "Files/tokenDocID.p", "wb" ) )
    # emptyFile = open("Files/tokenDocID.p", 'w')
    # emptyFile.close()
    with open( "Files/tokenDocID.p", "wb" ) as handle:
        pickle.dump(GlobalDictForWordFreq, handle)
    # data_string = pickle.dumps(GlobalDictForWordFreq)
    # tokenDocID.write(data_string)
    # for key,value in GlobalDictForWordFreq.items():
    #     tempString = str(key) + ", " + str(value) + newLine
    #     tokenDocID.write(tempString)

    # tempString = ""
    # tokenDocFreq.seek(0)
    # print JuLiDoTheThing.items()
    # emptyFile = open("Files/tokenDocFreq.p", 'w')
    # emptyFile.close()
    # pickle.dump( JuLiDoTheThing, open( "Files/tokenDocFreq.p", "wb" ) )
    with open( "Files/tokenDocFreq.p", "wb" ) as handle:
        pickle.dump(JuLiDoTheThing, handle)
    # data_string = pickle.dumps(JuLiDoTheThing)
    # tokenDocFreq.write(data_string)
    # for key,value in JuLiDoTheThing.items():
    #     tempString = str(key) + ", " + str(value) + newLine
    #     tokenDocFreq.write(tempString)

    # WRITING TO FILE: linksQueue.txt
    # Re-writes all of the lines.
    linksQueue.seek(0)
    linksQueue.write(linksQ.toString())

# Finds all of the links in a given URL and stores them
# in a queue.
def getLinks(i, limit):
    global j
    global visitedHash
    global JuLiDoTheThing
    global GlobalDictForWordFreq
    last = False
    while (i < limit):
    # if (i < limit):
        TempDictForWordFreq = dict()
        # This if statement writes to the file when the document counter is
        # divisible by 500.

        if (i%500==0 and i!=0):
            print "I am going to write to the file because we've hit a mulitple of 500! WHOOOO!!!"
            writeToFile(last)

        ## This try catch block allows the file to be written to, even if the
        ## queue is empty, or the link is unable to be opened.
        ## TODO: Make sure that if the queue is empty, it isn't an infinite loop.

        try:
            # Get the next URL on the queue and open it
            url = linksQ.dequeue()
        except:
            print "The queue is empty!! Good for you!!"
            writeToFile(last)
            return

        if(delay):
            t0 = time.time()
            slowDown()
        try:
            # html = urllib.urlopen(url, timeout=4).read()
            html = urllib.urlopen(url).read()
            soup = BeautifulSoup(html)
        except:
            print "You couldn't open the URL:", url
            # i += 1
            # writeToFile(last)
            last = True
            # getLinks(i, limit)
            continue

        # print "Here is the url we are checking: " + url
        # print "When you try to get the visisted hash link file:", visitedHash.get(url, False)
        # print ""
        # If we have visited the URL before, do not find the links a second time
        if (visitedHash.get(url, False) != False):
            i+=1
            print "You've already been to " + str(i), url

            # Instead, move to the next url in the queue
            continue

        # If it is a new URL, find the links and tokens in the webpage
        else:
            for link in soup.findAll('a'):
                    # Gets the new URLs for each webpage
                    newLink = (link.get('href'))
                    if (newLink != None):

                        # Check if the URL is absolute or relative
                        if(len(newLink)>7 and (re.match(r"http\:\/\/", newLink[0:7]) or re.match(r"https\:\/\/", newLink[0:8]))):
                            if(re.search(r"muhlenberg", newLink)):
                                if not(re.search(r"\#", newLink)):
                                    try:
                                        ## Checks to make sure the the URLs being added
                                        ## are not PDF files.
                                        if not (re.match(r".*.pdf$", str(newLink)) or re.match(r".*sync\.muhlenberg\.edu.*", str(newLink)) or re.match(r".*capstone.*", str(newLink)) or re.match(r".*blogs.*", str(newLink)) or re.match(r"http://www.muhlenberg.edu\w+.html", str(newLink))):
                                            if not (re.match(r".*javascript.*", str(newLink)) or re.match(r".*webapp.*", str(newLink)) or re.match(r".*edumailto.*", str(newLink))):
                                                add = True
                                                for nope,value in evadeAndConquor.items():
                                                    # print nope
                                                    if re.search(r".*" + nope + r".*", str(newLink)):
                                                        add = False
                                                        # print "found it", nope
                                                if add:
                                                    # If the link has not been visited before,
                                                    # add it to the queue.
                                                    if (visitedHash.get(newLink, False) == False):
                                                        linksQ.enqueue(newLink)
                                    except:
                                        print "Your URL is not a string:", newLink

                        else:
                            if not(re.search(r"\#", newLink)):
                                ## TODO: MAKE SURE THIS WORKS FOR EVERY CASE.
                                end = url.find(r'/', 7)
                                newLink = url[0:end] + newLink
                                try:
                                    ## Checks to make sure the the URLs being added
                                    ## are not PDF files.
                                    if not (re.match(r".*.pdf$", str(newLink)) or re.match(r".*sync\.muhlenberg\.edu.*", str(newLink)) or re.match(r".*capstone.*", str(newLink)) or re.match(r".*blogs.*", str(newLink)) or re.match(r"http://www.muhlenberg.edu\w+.html", str(newLink))):
                                        if not (re.match(r".*javascript.*", str(newLink)) or re.match(r".*webapp.*", str(newLink)) or re.match(r".*edumailto.*", str(newLink))):
                                            add = True
                                            for nope,value in evadeAndConquor.items():
                                                # print nope
                                                if re.search(r".*" + nope + r".*", str(newLink)):
                                                    add = False
                                                    # print "found it", nope
                                            if add:
                                                # If the link has not been visited before,
                                                # add it to the queue.
                                                if (visitedHash.get(newLink, False) == False):
                                                    linksQ.enqueue(newLink)
                                except:
                                    print "Your URL is not a string:", newLink


            i += 1
            tempDoc = open("Files/Documents/doc" + str(i) +".txt", 'w')
            for line in soup.prettify():
                tempDoc.write(line)

            tempDoc.close()
            # This will find all of the tokens in the file and store them in
            # a hash of tokens with their doc# and freq (TempDictForWordFreq) and
            # a hash of tokens and how many docs they appear in and which
            for line in soup.findAll('p'):
                    if not line.find('iframe'):
                        line = line.text
                        if not (re.match(r"http\:\/\/.*", line)):
                            if (line != None):
                                words = line.split(' ')
                                for word in words:
                                    if(re.search(r"\.([com]|[org]|[net]|[int]|[edu]|[gov])", word)):
                                        word = word.replace(word, "")
                                    ## TODO: Maybe remove hypens?
                                    # token = re.sub(r"and", "", word)
                                    token = re.sub(r"&\w*;", "", word)
                                    token = re.sub(r"[^A-Za-z\']*", "", token)
                                    token = re.sub(r"[\t]", "", token)
                                    token = token.lower()
                                    if(token != "" and token !=  " "):
                                        if(stemWords):
                                            token = stemmer.lemmatize(token, 'v')
                                            token = stemmer.lemmatize(token, 'n')

                                        token = token.strip()

                                        if(len(token)>1):
                                            if (removeStopWords):
                                                ## If the token isnt a stop word, add it.
                                                if (stopWords.get(token, False) == False):
                                                    if not re.search(r'\r\n', token):
                                                        TempDictForWordFreq[token] = int(TempDictForWordFreq.get(token, 0)) + 1
                                                        GlobalDictForWordFreq[token] = int(GlobalDictForWordFreq.get(token, 0)) + 1

                                            else:
                                                TempDictForWordFreq[token] = int(TempDictForWordFreq.get(token, 0)) + 1
                                                GlobalDictForWordFreq[token] = int(GlobalDictForWordFreq.get(token, 0)) + 1

            j += 1
            i = j

            for key, val in TempDictForWordFreq.items():
                # print "current word", key
                # print "was it found in the perminate dictionary", JuLiDoTheThing.get(key, False) != False
                if (JuLiDoTheThing.get(key, False) != False):
                    FerricksList = JuLiDoTheThing.get(key, False)
                    FerricksList.append([i,val])
                    JuLiDoTheThing[key] = FerricksList
                else:
                    FerricksList = list()
                    FerricksList.append([i,val])
                    JuLiDoTheThing[key] = FerricksList

            # If we haven't visited the file before, add it to the visitedHash
            # if (visitedHash.get(url, False) == False):
            visitedHash[url.strip()] = i

            print "Document", i, "has been processed."
            last = False

            # Call getlinks on the next document in the queue
            # getLinks(i, limit)




def writeToFile(last):
    # print "I'm writing to the file early because I love you. It is triggered by doc number " + str(i) + " URL: " + str(key)
    print "I'm writing to the file early because I love you."
    if(last==False):
        newLine = '\n'
        # visitedLinks.seek(0)
        # pickle.dump( visitedHash, open( "Files/visitedLinks.p", "wb" ) )
        #
        # tokenDocID.seek(0)
        # pickle.dump( GlobalDictForWordFreq, open( "Files/tokenDocID.p", "wb" ) )
        #
        # tokenDocFreq.seek(0)
        # pickle.dump( JuLiDoTheThing, open( "Files/tokenDocFreq.p", "wb" ) )

        with open('Files/visitedLinks.p', 'wb') as handle:
            pickle.dump(visitedHash, handle)

        with open( "Files/tokenDocID.p", "wb" ) as handle:
            pickle.dump(GlobalDictForWordFreq, handle)


        with open( "Files/tokenDocFreq.p", "wb" ) as handle:
            pickle.dump(JuLiDoTheThing, handle)

        # WRITING TO FILE: linksQueue.txt
        # Re-writes all of the lines.
        linksQueue.seek(0)
        linksQueue.write(linksQ.toString())


class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        try:
            self.items.index(item)
        except ValueError:
            self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def toString(self):
        if(self.isEmpty()==False):
            string = ""
            for item in self.items:
                if item != "":
                    string += item.strip() + '\n'
                else:
                    string += item.strip() + '\n'
            return string
        return ""


j = 0
# Create the queue here to make it global.
linksQ=Queue()
main()          # Calls the main function
# visitedLinks.close()
linksQueue.close()
# tokenDocID.close()
# tokenDocFreq.close()
