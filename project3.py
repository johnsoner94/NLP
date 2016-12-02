## Project: Project 3
## Class: CSI-382: NLP
## Creator: Emily Johnson
## Date Created:    November 5, 2015
## Date Edited:     November 10, 2016
## Date Finished:   ????
## Description: Originally created for CSI-210: Software Engineering for the
##              Pick A Flick Project, but was then repurposed for CSI-382: NLP.
##         NOW: It goes through the Muhlenberg website and stores the HTML,
##              while adding the links to other websites to a stack that will be
##              added later.
##  IT USED TO: scrape IMDb and adds values to a database.

import re       # Imports RegEx
import urllib   # Imports the ability to download files from URLs
import urllib2  # Ability to use URLS
import requests # Requests allow HTTP/1.1 requests
import time
# import HTMLParser
from nltk.corpus import wordnet #For word stemming
from nltk.stem import WordNetLemmatizer #For word stemming

from BeautifulSoup import BeautifulSoup # Import ability to scrape websites BeautifulSoup3

## TODO:
##       - Modify beenThereDoneThat.txt to include /robots.txt
##       - Delay the crawler so our IP address doesn't get banned.
##       - Adding another data stucture/file that stores the number of docs a
##         word appears in, as well as which documents the word appears in.
            ## TODO: START HERE LOVELY LADIES!!
##          - Deal when there are already values in the tokenByDocFreq.txt
## TEST:
##       - Make all of the words lowercase
##       - Add booleans to turn stops and stemming on and off.
##       - Write to your file every time:
##          ~ Unsucessful opening the web page.
##          ~ Stack is empty.
##          ~ Write to your file every x documents.

# GLOBAL: Count of the number of existing urls in visitedFile
# j = 0
# int j


# Global to convert HTML symbols to string
# h = HTMLParser()

# Setting the null value
NULL = None

# Global hash of stop words.
stopWords = dict()

# Global hash of tokens.
# Master Cheif Junior
# tokenMasterHash = dict()

# Open up the global token file.
tokenDocIDFile = open("tokenByDocID.txt", 'a+')

# Open up the global token file.
tokenDocFreqFile = open("tokenByDocFreq.txt", 'r+')

# Global hash of tokens with their doc frequency.
tokenDocFreqHash = dict()

# Global hash of visited sites.
visitedHash = dict()

# Open up the global visited sites file.
visitedFile = open("beenThereDoneThat.txt", 'r+')

# Open the global links queue file.
linksFile = open("linksQueue.txt", 'r+')

# Our instance of stemmer.
stemmer = WordNetLemmatizer()

# Boolean switches to turn off stop words and stemming words.
removeStopWords = True
stemWords = True

def slowDown():
    time.sleep(5)

# Calls getLinks for the first time from whatever the root URL is
# (currently muhlenberg.edu)
def main():
    global j
    j = 0
    url = 'http://www.muhlenberg.edu/'
    linksQ.enqueue(url)
    # print(linksQ.toString())
    limit = 6
    i = 0
    stopIntheNameofWords = open("stopwords.txt", 'r')
    # print stopIntheNameofWords.readlines()
    for word in stopIntheNameofWords:
        word = str(word)
        # print type(word), word
        stopWords[word.strip()] = stopWords.get(word.strip(), 0) + 1
    stopIntheNameofWords.close()

    # Go through the file and convert each line to a key and value pair, with
    # the key being the url and the value being it's document number.
    for line in visitedFile:
        line = str(line)
        line = line.split(", ")
        j+=1
        # print j
        # print "Hey, we are running the for loop in 64"
        # print "The line is this:",line
        visitedHash[line[0]] = line[1]
        # print ""
    # visitedFile.close()

    # print visitedHash

    for line in linksFile:
        line = str(line)
        linksQ.enqueue(line)
    # linksFile.close()
    # for line in tokenDocIDFile:
    #     tokenList = line.split(", ")
    #     tokenMasterHash[tokenList[0]] = [tokenList[1], tokenList[2]]

    # print "Line 131"
    # try:
    #     tokenByDocFreqFile = open("tokenByDocFreq.txt", "r")
    #     print "Line 134"
    # except:
    #     print "Nope, you're not open tokenByDocFreq.txt today!!"
    # print tokenDocFreqFile
    print tokenDocFreqFile.readlines()
    # counter = 0
    # print "Line 139"
    for line in tokenDocFreqFile.readlines():
        line = str(line)
        line = line[1:len(line)-2]
        line = line.split("], [")

        ## NOTE THIS IS THE PROBEL M RWT:??GR?G
        ## HOW COME LINE[2] IS THE LISR?????????????????????
        print "this is a goode thing:):):):)):",line[3]

        line[3] = line[3].split(", ")
        try:
            docNumbers = map(int, line[3])
        except:
            docNumbers = list(map(int, line[3]))

        tempList = [int(line[1]),line[2], docNumbers]
        tokenDocFreqHash[line[0].strip()] = tempList
    # tokenByDocFreqFile.close()
    # print tokenByDocFreqFile.readlines()
    # print "Line 153"


    #Get the links for the next document ????
    getLinks(i, limit+j)

    # WRITING TO FILE: beenThereDoneThat.txt
    # Re-writes all of the lines.
    newLine = '\n'
    # visitedFileAdd = open("beenThereDoneThat.txt", 'w')
    for key,value in visitedHash.items():
        # print "Hey, we are running the for loop in 90"
        tempString = str(key) + ", " + str(value)
        # print "The tempstring is this:",tempString
        # print ""
        visitedFile.write(tempString.strip())
        visitedFile.write(newLine)

    # WRITING TO FILE: tokenByDocFreq.txt
    # Adds values to the end of the
    # Add each token from the token by doc freq hash to tokenByDocFreq.txt
    for key,value in tokenDocFreqHash.items():
        numString = value[2]
        # numString = ""
        # for num in value[1]:
        #     numString += num + ", "
        try:
            tempString = "[" + str(key) + "], [" + str(value[0]) + "], [" + str(value[1]) + "], " + str(numString) + newLine
            tokenDocFreqFile.write(tempString)
        except:
            print "Key:", key
            print "Value:", value
            print "J:", j

    # WRITING TO FILE: linksQueue.txt
    # Re-writes all of the lines.
    # linksWrite = open("linksQueue.txt", 'w')
    linksFile.write(linksQ.toString())

# Finds all of the links in a given URL and stores them
# in a queue.
def getLinks(i, limit):
    global j
    if (i < limit):
        tokenTemp = dict()
        # docNumRepresent = False
        # This if statement writes to the file when the document counter is
        # divisible by 500.
        if (i%500==0 and i!=0):
            writeToFile(tokenTemp, i)
        ## This try catch block allows the file to be written to, even if the
        ## queue is empty, or the link is unable to be opened.
        ## TODO: Make sure that if the queue is empty, it isn't an infinite loop.
        try:
            # Get the next URL on the queue and open it
            url = linksQ.dequeue()
        except:
            writeToFile(tokenTemp, i)
            return;
        try:
            # response = requests.get(url)
            # response = requests.get(url, allow_redirects=True)
            # html = response.content
            t0 = time.time()
            slowDown()
            html = urllib.urlopen(url).read()
            soup = BeautifulSoup(html)
        except:
            writeToFile(tokenTemp, i)
            getLinks(i, limit)
            return;


        # print linksQ.toString()

        # If we have visited the URL before, do not find the links a second time
        if (visitedHash.get(url, False) != False):
            # print "************HERE*********"
            i+=1
            # limit +=1

            # Instead, move to the next url in the queue
            getLinks(i, limit)

        # If it is a new URL, find the links and tokens in the webpage
        else:
            # if (visitedHash.get(url, False) == False):
            #     getLinks(i, limit)

            for link in soup.findAll('a'):
                # if (link != None):
                #     title = link.text
                #     if(title == ""):
                #         title = ""
                #     # else:
                #         # print title

                    # Gets the new URLs for each webpage
                    newLink = (link.get('href'))
                    if (newLink != None):

                        # Check if the URL is absolute or relative
                        if(len(newLink)>7 and (re.match(r"http\:\/\/", newLink[0:7]) or re.match(r"https\:\/\/", newLink[0:8]))):
                            if(re.search(r"muhlenberg", newLink)):
                                if not(re.search(r"\#", newLink)):

                                    # If the link has not been visited before,
                                    # add it to the queue.
                                    # if (visitedHash.get(newLink, False) == False):
                                        # print newLink
                                        linksQ.enqueue(newLink)

                        else:
                            if not(re.search(r"\#", newLink)):
                                ## TODO: MAKE SURE THIS WORKS FOR EVERY CASE.
                                # print "BEFORE: " + newLink
                                # print "URL: " + url
                                # end = url.rfind(r'/', 1)
                                end = url.find(r'/', 7)
                                newLink = url[0:end] + newLink
                                # print "AFTER: " + newLink
                                # print newLink
                                # print visitedHash
                                # print newLink

                                # If the link has not been visited before,
                                # add it to the queue.
                                if (visitedHash.get(newLink, False) == False):
                                    linksQ.enqueue(newLink)



            j += 1
            i = j
            # This will find all of the tokens in the file and store them in
            # a hash of tokens with their doc# and freq (TokenTemp) and
            # a hash of tokens and how many docs they appear in and which
            for line in soup.findAll('p'):
                line = line.text
                if (line != None):
                    # print line
                    words = line.split(' ')
                    for word in words:
                        # print "WORD UNCHANGED: " + word
                        # token = h.unescape(word)
                        # print ["WORD CHANGED: ", token]
                        # token = token.replace("'", "")
                        # token = word.replace(r"&\w*;", "")
                        # token = word.replace("|", "")
                        # token = token.replace(")", "")
                        # token = token.replace("(", "")
                        # token = token.replace(",", "")
                        ## TODO: Maybe remove hypens?
                        # token = token.replace("-", "")
                        token = re.sub(r"&\w*;", "", word)
                        token = re.sub(r"[^A-Za-z\s\']*", "", token)
                        token = token.lower()
                        if(stemWords):
                            #Look through all the word and convert them as if they are verbs
                            token = stemmer.lemmatize(token, 'v')
                            #Look at that returned word and fix all the ones that weren't verbs (nouns)
                            token = stemmer.lemmatize(token, 'n')
                        token = token.strip()
                        if(len(token)>1):
                            # if(re.search(r"\\x", str([token]))):
                            #     token = token[1:]
                            if (removeStopWords):
                                ## If the token is a stop word, don't add it.
                                if (stopWords.get(token, False)== False):
                                    ## Adds the token to the toekbyDocID
                                    ## dictionary, which tempoary, and is
                                    ## recreated in each call to getLinks.
                                    ## token = frequency of the word in the current document
                                    ## NOTE: The document number is i, and will
                                    ## be added later when the dictionary is
                                    ## written to the csv file.
                                    tokenTemp[token] = tokenTemp.get(token, 0) + 1

                                    ## Checks to see if the token already exists
                                    ## in the tokenByDocFreqHash, if it doesn't,
                                    ## then the list is created, and the current
                                    ## doc number, i, is added to the docNums.
                                    #if (docNumRepresent == False):
                                    if (tokenDocFreqHash.get(token, [NULL, NULL,NULL])[2] == NULL):
                                        # if (docNumRepresent == False):
                                        docNums = list()
                                        docNums.append(i)

                                        freq = tokenTemp[token]

                                        ## Checks to see if the word already exists
                                        ## in the tokenByDocFreqHash and added by one.

                                        # numOfDocs = len(docNums)

                                        # print "The word was not found", docNums
                                    ## Else, the list is accessed and then
                                    ## appended to add the current doc number, i.
                                    else:
                                        docNums = tokenDocFreqHash.get(token, [NULL, NULL, NULL])[2]
                                        freq = tokenDocFreqHash.get(token, [NULL, NULL, NULL])[1]

                                        # print "The word was found", docNums
                                        if (docNums[len(docNums)-1] !=i):
                                            docNums.append(i)

                                            freq = int(freq) + tokenTemp[token]
                                            ## Checks to see if the word already exists
                                            ## in the tokenByDocFreqHash and added by one.

                                            # numOfDocs = len(docNums)
                                    tempList = [len(docNums), freq, docNums]
                                    tokenDocFreqHash[token] = tempList

                            else:
                                tokenTemp[token] = int(tokenTemp.get(token, 0)) + 1
                                ## TODO: WHEN THE ABOVE CODE IS BUG FREE, DUPLICATE IT HERE FOR WHEN THE BOOLEAN SWITCH FOR STOP WORDS IS TURNED OFF.





            # print(linksQ.toString())
            # print "-----------------"
            #TODO: ADD THE DICTIONARY TO A FILE
            newLine = '\n'

            # If we haven't visited the file before, add it to the visitedFileHash
            if (visitedHash.get(url, False) == False):
                visitedHash[url.strip()] = i

            # WRITING TO FILE: tokenByDocID.txt
            # Adds values to the end of the
            # Add each token from the token by doc ID hash to tokenByDocID.txt
            for key,value in tokenTemp.items():
                try:
                    tempString = str(key) + ", " + str(value) + ", " + str(i) + newLine
                    # print tempString
                    # tempString = str(key.encode("utf-8")) + ", " + str(value) + ", " + str(i)
                    tokenDocIDFile.write(tempString)
                except:
                    print "Key:", key
                    print "Value:", value
                    print "J:", j


            # Call getlinks on the next document in the queue
            getLinks(i, limit)




def writeToFile(tokenTemp, i):
    # print "I'm writing to the file early because I love you. It is triggered by doc number " + str(i) + " URL: " + str(key)
    print "I'm writing to the file early because I love you. It is triggered by doc number " + str(i)
    # WRITING TO FILE: beenThereDoneThat.txt
    # Re-writes all of the lines.
    newLine = '\n'
    visitedFileAdd = open("beenThereDoneThat.txt", 'w')
    for key,value in visitedHash.items():
        # print "Hey, we are running the for loop in 90"
        tempString = str(key) + ", " + str(value)
        # print "The tempstring is this:",tempString
        # print ""
        visitedFileAdd.write(tempString.strip())
        visitedFileAdd.write(newLine)

    # WRITING TO FILE: linksQueue.txt
    # Re-writes all of the lines.
    linksWrite = open("linksQueue.txt", 'w')
    linksWrite.write(linksQ.toString())

    # WRITING TO FILE: tokenByDocID.txt
    # Adds values to the end of the
    # Add each token from the token by doc ID hash to tokenByDocID.txt
    for key,value in tokenTemp.items():
        try:
            tempString = str(key) + ", " + str(value) + ", " + str(i) + newLine
            # print tempString
            # tempString = str(key.encode("utf-8")) + ", " + str(value) + ", " + str(i)
            tokenDocIDFile.write(tempString)
        except:
            print "Key:", key
            print "Value:", value
            print "J:", j


    # WRITING TO FILE: tokenByDocID.txt
    # Adds values to the end of the
    # Add each token from the token by doc ID hash to tokenByDocID.txt
    for key,value in tokenTemp.items():
        try:
            tempString = str(key) + ", " + str(value) + ", " + str(i) + newLine
            # print tempString
            # tempString = str(key.encode("utf-8")) + ", " + str(value) + ", " + str(i)
            tokenDocIDFile.write(tempString)
        except:
            print "Key:", key
            print "Value:", value
            print "J:", j


    # visitedFileAdd.close()
    # linksWrite.close()



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


j = 0
# Create the queue here to make it global.
linksQ=Queue()
main()          # Calls the main function
visitedFile.close()
linksFile.close()
tokenDocIDFile.close()
tokenDocFreqFile.close()
