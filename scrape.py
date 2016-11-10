## Project: Scrape
## Class: CSI-382: NLP
## Creator: Emily Johnson
## Date Created: November 5, 2015
## Date Edited:  November 10, 2016
## Description: Originally created for CSI-210: Software Engineering for the
##              Pick A Flick Project, but was then repurposed for CSI-382: NLP.
##              THIS IS A TESTING ZONE, CODE THAT IS HELPFUL GOES TO project3.py
##         NOW: It goes through the Muhlenberg website and stores the HTML,
##              while adding the links to other websites to a stack that will be
##              added later.
##  IT USED TO: scrape IMDb and adds values to a database.

import re       # Imports RegEx
import psycopg2 # Imports access to database
import urllib # Imports the ability to download files from URLs
import urllib2 # Ability to use URLS
import requests # Requests allow HTTP/1.1 requests
from BeautifulSoup import BeautifulSoup # Import ability to scrape websites BeautifulSoup3

# Setting the null value
NULL = None

# When on my computer I use a Postgres database, I put everything on here and then import
# it because I could not import the modules onto the MathCS server. I would do a dump of
# the databases created and then run a script to important the data onto the database on
# the MathCS server. Dr. Benjamin helped our group with this and made it possible.

# Checks to make sure that the database can be connected to before excuting the rest of
# the program, also does this before anything else
# try:
#     conn = psycopg2.connect("dbname='template1' user='' host='localhost'")
# except:
#     print "I am unable to connect to the database"

# Set the cursor
# cur = conn.cursor()

# Gets the movies and tags, then commits whatever changes have been made
def main():
    getLinks()
    # conn.commit()

# Goes to the Top 250 on IMDb and scrapes the title, year, the link to movie's IMDb page
# calls the rating, duration, and posters functions
def getLinks():
    url = 'http://www.muhlenberg.edu/'
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)
    col = 0

    for ultag in soup.findAll('ul'):
        for litag in ultag.findAll('li'):
            # print litag.text


        # # Increases the column so that each movie has its own section in the table
        # col = col + 1
        #
            # Gets the information of each movies that is most easily accessible on the
            # list of movies.
            if (litag.a != None):
                title = litag.a.text
                title = title.replace("'", "''");
                # print title

                # Gets the new URL for each movie.
                newLink = (litag.a.get('href'))
                if(re.match(r"http\:\/\/", newLink[0:7])):
                    # newLink = "http://www.muhlenberg.edu/" + newLink
                    print newLink
                else:
                    newLink = "http://www.muhlenberg.edu" + newLink
                    print newLink

        # These call the methods that have to access the information in different parts of the movie's
        # individual page.
        #rating = getRating(col, newLink)
        #dur = getDuration(col, newLink)
        #getPoster(col, newLink, title)
        #poster = getPoster(col, newLink, title)
        #print poster


        # Inserts a new movie into the table
##        try:
##            cur.execute("INSERT INTO movTest (title, year, rating, duration, poster) VALUE, %s, %s, %s, %s)", (title, year, rating, dur, poster))
##        except:
##            print "Error adding movie to table"


        # Parameters are the link and the title and then in adds the different tags
        # getTags(newLink, title, "movTest", "tagTest")


## Parameter: Get the movie ID, Movie URL
## adds the different tag types to the table for the given movie
def getTags(newLink, title, tableMovie, tableTag):
    ## Attemps to cast the title to a string
    try:
        title = str(title)
    except:
        print "Error converting " , type(title) , " to a string."

    # Adds ' to the title so that it can be given as an SQL command
    title = "'" + title + "'"
    command = "SELECT * FROM movTest WHERE title = " + title + ";"
    # If the movie cannot be found, the function is exited
    try:
        cur.execute(command)
    except:
        print "Cannot find column in the movie table."
        print "Command that didn't work: " + command
        return

    rows = cur.fetchall()


    # Calls the function for adding the tags for the genre, director, creators, actors, and keywords
    for row in rows:
        movie_ID = row[0]
        getGenre(movie_ID, newLink, title, "tagTest")
        getDirector(movie_ID, newLink, title, "tagTest")
        getCreators(movie_ID, newLink, title, "tagTest")
        getActor(movie_ID, newLink, title, "tagTest")
        getKeywords(movie_ID, newLink, title, "tagTest")

# Returns the rating for given movie
def getRating(col, url):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)

    # In this case limit 1 is intentional and neccessary
    for rating in soup.findAll(attrs={"itemprop": "contentRating"}, limit=1):
        rate = rating.get('content')
        return rate


# Returns the duration for given movie
def getDuration(col, url):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)

    # In this case limit 1 is intentional and neccessary
    for dur in soup.findAll(attrs={"itemprop": "duration"}, limit=1):
        duration = dur.text
        duration = duration.rstrip(" min")
        #print duration
        return duration


# Downloads the poster into Posters folder and returns the file location based off of the title of the movie
def getPoster(col, url, title):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)

    for img in soup.findAll("img", attrs={"height": "317"}):
        poster = img.get("src")
        title = title.replace(' ', '')
        location = "Posters/" + title + ".jpg"
        urllib.urlretrieve(poster, location)
        return location
    # Can update the location of a poster if need be
##        col = str(col)
##        location = location.replace("'", "''")
##        location = "'" + location + "'"
##        command = ("UPDATE movtest SET poster = " + location + " WHERE id = " + col + ";")
##        try:
##            print command
##            #cur.execute(command)
##        except:
##            print "Command failed, update poster url"
##            return



# Add the genres of a given movie as a type of tag
def getGenre(movie_ID, url, title, tableTag):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)

    # Finds all of the given genres for a movie
    for gen in soup.findAll("span", attrs={"itemprop": "genre"}):
        genre = gen.text
        genre = genre.replace("'", "''")
        genre = "'" + genre + "'"

        # Attempts to check to make sure that genre doesn't already exist, exits the function if it cannot
        command = ("SELECT CASE WHEN EXISTS (SELECT * FROM tagTest WHERE name = " + genre + ") THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END;")


        try:
            cur.execute(command)
            result = cur.fetchall()[0]
            exists = result[0]
            exists = int(exists)
        except:
            print "Command failed, genre"
            return


         # If it does not exist
        if exists == 0:
            genre = genre[1: -1]        # Format the genre by removing the ' a the beginning at the end of the genre variable
            try:
                genre = str(genre)      # Try to format the genre into a string
            except:
                print "Error converting " , type(genre) , " to a string."

            # Because it didn't exist, at it to the tag table. Then select that tag from the table, so that you can add it to the pairing table
            try:
                cur.execute("INSERT INTO tagTest (name, type) VALUES (%s, %s);", (genre, 'genre'))
                genre = "'" + genre + "'"
                command = "SELECT * FROM tagTest WHERE name = " + genre + ";"
                cur.execute(command)
            except:
                print "Adding the tag to the table didn't work"
                print command
                return
        # If it does exist select it from the tag table
        else:
            command = "SELECT * FROM tagTest WHERE name = " + genre + ";"
            try:
                cur.execute(command)
            except:
                print "Cannot find column in the tag table."
                return

        rows = cur.fetchall()

        # Add the movie_ID and the tag_ID as a new pairing in the pairing table, if that pairing doesn't already exist
        for row in rows:
            tag_ID = row[0]

            try:
                tag_ID = str(tag_ID)
            except:
                print "Error converting " , type(tag_ID) , " to a string."

            try:
                movie_ID = str(movie_ID)
            except:
                print "Error converting " , type(movie_ID) , " to a string."

            command = ("SELECT CASE WHEN EXISTS (SELECT * FROM pairingTest WHERE tag_ID = " + tag_ID + " AND movie_ID = " + movie_ID + ") THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END;")

            try:
                cur.execute(command)
                result = cur.fetchall()[0]
                exists = result[0]
                exists = int(exists)
                command = ("SELECT CASE WHEN EXISTS (SELECT * FROM tagTest WHERE name = " + genre + ") THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END;")
                if exists == 0:
                    try:
                        command = ("INSERT INTO pairingTest (tag_ID, movie_ID) VALUES (" + tag_ID + ", " + movie_ID + ");")
                        cur.execute(command)
                    except:
                        print "Error adding genre pair: " + command
                else:
                    return
            except:
                command = str(command)
                print "Error checking for genre pair: " + command


# Add the directors of a given movie as a type of tag
def getDirector(movie_ID, url, title, tableTag):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)

    # Finds all of the given directors for a movie
    for direct in soup.findAll(attrs={"itemprop": "director"}):
        director = direct.a.text
        director = director.replace("'", "''")
        director = "'" + director + "'"
        # Attempts to check to make sure that director doesn't already exist, exits the function if it cannot
        command = ("SELECT CASE WHEN EXISTS (SELECT * FROM tagTest WHERE name = " + director + ") THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END;")
        try:
            cur.execute(command)
            result = cur.fetchall()[0]
            exists = result[0]
            exists = int(exists)
        except:
            print "Command failed, director"
            return

        # If it does not exist
        if exists == 0:
            director = director[1: -1]      # Format the director by removing the ' a the beginning at the end of the director variable
            try:
                director = str(director)    # Try to format the director into a string
            except:
                print "Error converting " , type(director) , " to a string."
            # Because it didn't exist, at it to the tag table. Then select that tag from the table, so that you can add it to the pairing table
            try:
                cur.execute("INSERT INTO tagTest (name, type) VALUES (%s, %s);", (director, 'director'))
                director = "'" + director + "'"
                cur.execute("SELECT * FROM tagTest WHERE name = " + director + ";")
            except:
                print "Adding the tag to the table didn't work"
        # If it does exist select it from the tag table
        else:
            command = "SELECT * FROM tagTest WHERE name = " + director + ";"
            try:
                cur.execute(command)
            except:
                print "Cannot find column."
                return

        rows = cur.fetchall()

        # Add the movie_ID and the tag_ID as a new pairing in the pairing table, if that pairing doesn't already exist
        for row in rows:
            tag_ID = row[0]

            try:
                tag_ID = str(tag_ID)
            except:
                print "Error converting " , type(tag_ID) , " to a string."

            try:
                movie_ID = str(movie_ID)
            except:
                print "Error converting " , type(movie_ID) , " to a string."
            command = ("SELECT CASE WHEN EXISTS (SELECT * FROM pairingTest WHERE tag_ID = " + tag_ID + " AND movie_ID = " + movie_ID + ") THEN CAST (1 AS BIT) ELSE CAST(0 AS BIT) END;")
            try:
                cur.execute(command)
                result = cur.fetchall()[0]
                exists = result[0]
                exists = int(exists)

                if exists == 0:
                    try:
                        command = ("INSERT INTO pairingTest (tag_ID, movie_ID) VALUES (" + tag_ID + ", " + movie_ID + ");")
                        cur.execute(command)
                    except:
                        print "Error adding director pair: " + command
                else:
                    return
            except:
                print "Error checking for directoring pair: " + command



# There's an error in the logic. If a name has already been added as a tag under one category, it is not readded under the new category. (ie Frank Darabont is both a director
# and a writter for The Shawshank Redemption, but he'll only be credited as a writer.) If I were to fix this method, I think all of the other methods would have to be modified
# to be able to be cross referenced.

# Add the cretors of a given movie as a type of tag
def getCreators(movie_ID, url, title, tableTag):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)

    # Finds all of the given creators for a movie
    for create in soup.findAll("span", attrs={"itemprop": "name"}):
        prev = ""
        names = create.parent.parent.attrs
        for writers in names:
            check = str(writers[1])
            if prev == "txt-block":
                if "creator" == check:
                    creator = create.text
                    creator = creator.replace("'", "''")
                    creator = "'" + creator + "'"
                    # Attempts to check to make sure that creators doesn't already exist, exits the function if it cannot
                    command = ("SELECT CASE WHEN EXISTS (SELECT * FROM tagTest WHERE name = " + creator + ") THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END;")
                    try:
                        cur.execute(command)
                        result = cur.fetchall()[0]
                        exists = result[0]
                        exists = int(exists)
                    except:
                        print "Command failed, creator"

                    # If it does not exist
                    if exists == 0:
                        try:
                            creator = str(creator)  # Try to format the creator into a string
                        except:
                            print "Error converting " , type(creator) , " to a string."
                        creator = creator[1: -1]    # Format the creator by removing the ' a the beginning at the end of the creator variable
                        # Because it didn't exist, at it to the tag table. Then select that tag from the table, so that you can add it to the pairing table
                        try:
                            cur.execute("INSERT INTO tagTest (name, type) VALUES (%s, %s);", (creator, 'creator'))
                            creator = "'" + creator + "'"
                            cur.execute("SELECT * FROM tagTest WHERE name = " + creator + ";")
                        except:
                            print "Adding the tag to the table didn't work"
                    # If it does exist select it from the tag table
                    else:
                        command = "SELECT * FROM tagTest WHERE name = " + creator + ";"
                        try:
                            cur.execute(command)
                        except:
                            print "Cannot find column."

                    rows = cur.fetchall()

                    # Add the movie_ID and the tag_ID as a new pairing in the pairing table, if that pairing doesn't already exist
                    for row in rows:
                        tag_ID = row[0]

                        try:
                            tag_ID = str(tag_ID)
                        except:
                            print "Error converting " , type(tag_ID) , " to a string."

                        try:
                            movie_ID = str(movie_ID)
                        except:
                            print "Error converting " , type(movie_ID) , " to a string."
                        command = ("SELECT CASE WHEN EXISTS (SELECT * FROM pairingTest WHERE tag_ID = " + tag_ID + " AND movie_ID = " + movie_ID + ") THEN CAST (1 AS BIT) ELSE CAST(0 AS BIT) END;")
                        try:
                            cur.execute(command)
                            result = cur.fetchall()[0]
                            exists = result[0]
                            exists = int(exists)

                            if exists == 0:
                                try:
                                    command = ("INSERT INTO pairingTest (tag_ID, movie_ID) VALUES (" + tag_ID + ", " + movie_ID + ");")
                                    cur.execute(command)
                                except:
                                    print "Error adding creator pair: " + command
                            else:
                                print "Does exist"
                        except:
                            print "Error checking for creating pair: " + command
            prev = check # Allows the scraping process to move through the website.



# Right now it only returns the top 15 actors in the movie.

# Add the actors of a given movie as a type of tag
def getActor(movie_ID, url, title, tableTag):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)

    count = 0

    # Finds all of the given actors for a movie
    for stars in soup.findAll(attrs={"itemprop": "actor"}):
        count = count + 1
        actor = stars.text
        actor = actor.replace("'", "''")
        actor = "'" + actor + "'"

        # Attempts to check to make sure that actor doesn't already exist, exists the function if it cannot
        command = ("SELECT CASE WHEN EXISTS (SELECT * FROM tagTest WHERE name = " + actor + ") THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END;")

        try:
            cur.execute(command)
            result = cur.fetchall()[0]
            exists = result[0]
            exists = int(exists)
        except:
            print "Command failed, actor: " + command
            return

        # If it does not exist
        if exists == 0:
            actor = actor[1: -1]    # Format the actor by removing the ' a the beginning at the end of the actor variable
            try:
                actor = str(actor)  # Try to format the actor into a string
            except:
                print "Error converting " , type(actor) , " to a string."

             # Because it didn't exist, at it to the tag table. Then select that tag from the table, so that you can add it to the pairing table
            try:
                cur.execute("INSERT INTO tagTest (name, type) VALUES (%s, %s);", (actor, 'actor'))
                actor = "'" + actor + "'"
                cur.execute("SELECT * FROM tagTest WHERE name = " + actor + ";")
            except:
                print "Adding the tag to the table didn't work"
        # If it does exist select it from the tag table
        else:
            command = "SELECT * FROM tagTest WHERE name = " + actor + ";"
            try:
                cur.execute(command)
            except:
                print "Cannot find column: " + command
                return

        rows = cur.fetchall()

        # Add the movie_ID and the tag_ID as a new pairing in the pairing table, if that pairing doesn't already exist
        for row in rows:
            tag_ID = row[0]

            try:
                tag_ID = str(tag_ID)
            except:
                print "Error converting " , type(tag_ID) , " to a string."

            try:
                movie_ID = str(movie_ID)
            except:
                print "Error converting " , type(movie_ID) , " to a string."
            command = ("SELECT CASE WHEN EXISTS (SELECT * FROM pairingTest WHERE tag_ID = " + tag_ID + " AND movie_ID = " + movie_ID + ") THEN CAST (1 AS BIT) ELSE CAST(0 AS BIT) END;")
            try:
                cur.execute(command)
                result = cur.fetchall()[0]
                exists = result[0]
                exists = int(exists)

                if exists == 0:
                    try:
                        command = ("INSERT INTO pairingTest (tag_ID, movie_ID) VALUES (" + tag_ID + ", " + movie_ID + ");")
                        cur.execute(command)
                    except:
                        print "Error adding actor pair: " + command
                else:
                    return
            except:
                print "Error checking for actor pair: " + command


# Add the keywords of a given movie as a type of tag
def getKeywords(movie_ID, url, title, tableTag):

    url = url + "keywords"
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)

    count = 0

    # Finds all of the given keywords for a movie
    for tag in soup.findAll(attrs={"class": "sodatext"}):
        count = count + 1
        tag = tag.text
        try:
            tag = str(tag)
        except:
            print "Error converting " , type(tag) , " to a string."

        tag = tag.replace("'", "''")
        tag = "'" + tag + "'"

        # Attempts to check to make sure that keyword doesn't already exist, exits the function if it cannot
        command = ("SELECT CASE WHEN EXISTS (SELECT * FROM tagTest WHERE name = " + tag + ") THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END;")
        try:
            cur.execute(command)
            result = cur.fetchall()[0]
            exists = result[0]
            exists = int(exists)
        except:
            print "Command failed, keywords"
            print command
            return

        # If it does not exist
        if exists == 0:
            tag = tag[1: -1]    # Format the keyword by removing the ' a the beginning at the end of the keyword variable
            tag = str(tag)      # Try to format the keyword into a string
            # Because it didn't exist, at it to the tag table. Then select that tag from the table, so that you can add it to the pairing table
            try:
                cur.execute("INSERT INTO tagTest (name, type) VALUES (%s, %s);", (tag, 'keyword'))
                tag = "'" + tag + "'"
                cur.execute("SELECT * FROM tagTest WHERE name = " + tag + ";")
            except:
                print "Adding the tag to the table didn't work"
                return
        # If it does exist select it from the tag table
        else:
            command = "SELECT * FROM tagTest WHERE name = " + tag + ";"
            try:
                cur.execute(command)
            except:
                print "Cannot find column."
                return

        rows = cur.fetchall()

        # Add the movie_ID and the tag_ID as a new pairing in the pairing table, if that pairing doesn't already exist
        for row in rows:
            tag_ID = row[0]

            try:
                tag_ID = str(tag_ID)
            except:
                print "Error converting " , type(tag_ID) , " to a string."

            try:
                movie_ID = str(movie_ID)
            except:
                print "Error converting " , type(movie_ID) , " to a string."
            command = ("SELECT CASE WHEN EXISTS (SELECT * FROM pairingTest WHERE tag_ID = " + tag_ID + " AND movie_ID = " + movie_ID + ") THEN CAST (1 AS BIT) ELSE CAST(0 AS BIT) END;")
            try:
                cur.execute(command)
                result = cur.fetchall()[0]
                exists = result[0]
                exists = int(exists)

                if exists == 0:
                    try:
                        command = ("INSERT INTO pairingTest (tag_ID, movie_ID) VALUES (" + tag_ID + ", " + movie_ID + ");")
                        cur.execute(command)
                    except:
                        print "Error adding keword pair: " + command
                        return
                else:
                    return
            except:
                print "Error checking for keyword pair: " + command
                return



main()          # Calls the main function
# cur.close()     # Closes the cursor
# conn.close()    # Closes the connection to the database
