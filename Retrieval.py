import math
# ??eyo
# Emily: We do have 10,000 docs!
countOfDocs = 10000

# This will be the user submission.
query = "Earth, Fire, Water, Air. Long ago, the nations lived in harmony. But then, the fire nation attacked."



## Emily: TODO: NOTE: QUESTION: HEY CASIE!!! I HAVE A QUESTION!!! WHY DON'T WE
##        EVERY LOOK AT THE DOCUMENTS TOTAL NUMBER OF OCCURANCES IN ALL OF THE
##        DOCUMENTS?!!?!?!?!


# Initialize a dictionary to be used for the query values.
QueryWords = dict()

# Initialize a dictionary to be used to save the idf for each word in query.
# This is done to avoid having to recompute the idf for a certain word multiple
# times.
QueryIdf = dict()

# Initialize a dictionary to be used to save the tfidf for each word in query.
# This saves the final tfidf value to be used in the dot product and cosine
# similarity.
QueryTfIdf = dict()


# Initialize a dictionary of the documents that contain query words.
DocsThatContainQueryWords = dict()

# Initialize a dictionary that has each query word as a key and the count of
# docs it is in as the value (eyo should this be a list of the doc #'s its in?)
dfDictionary = dict()

# Initialize a dictionary for each document's cosine similarity. The key is the
# doc number and the val is the cosine similarity.
cosineSimDict = dict()


# Initialize the QueryNumForCosine, which will incrementally add to the
# ||Query|| value.
QueryNumForCosine = 0

# Initialize the DocNumForCosine, which will incrementally add to the
# ||Query|| value.
DocNumForCosine = 0

# Get the count of each word in the query, and also do some proprocessing
for word in query.split(" "):
    word = re.sub(r"&\w*;", "", word)
    word = re.sub(r"[^A-Za-z\']*", "", word)
    word = word.lower()
    QueryWords[word] = QueryWords.get(word, 0)) + 1

# Find the highest frequency value of a query
# Eyo does this work tho
maxFreq = max(QueryWords, key=lambda i: QueryWords[i])


# Look through the tokenByDocFreq list OR the JuLiDoTheThing dict(?) eyo
# and find any docs that contain the current query word. eyo I think we should
# eyo shoot for JuLiDoTheThing

for word,count in QueryWords.items():


    #Emily: I'm just a girl, trying to add dictionaries from a file to a program.
    try:
        with open( "Files/tokenDocFreq.p", "rb" ) as handle:
            JuLiDoTheThing = pickle.load(handle)
    except:
        print "File is empty."
    #Emily: I tried to go that extra mile and add the code so you could get all
    ##      of the documents that contain the query word.
    ##      docNumsAndFreq = [[doc1, wordFreqinDoc], [doc2, wordFreqinDoc]]
    docNumsAndFreq = JuLiDoTheThing.get(word, False)


    ## Emily: I think this will work?
    for item in docNumsAndFreq:
        docNum = int(item[0])
        docFreq = int(item[1])

        ## Emily: Casie coded all of this, I simply copy and pasted it.
        # If there is already an entry for that doc, add the word
        # and its corresponding doc freq as the value. Otherwise,
        # initialize the dictionary entry. For each doc
        # number, save the word found in it and that word's doc
        # frequency. EYO is this even right tho
        if (DocsThatContainQueryWords.get(docNum, False) != False):
            tempoList = DocsThatContainQueryWords[docNum]

            tempoList.append([word, docFreq])
            DocsThatContainQueryWords[docNum] = tempoList
        else:
            tempoList = list()
            tempoList.append([word, docFreq])
            DocsThatContainQueryWords[docNum] = tempoList

        # Add to the total count of times a word is in a doc.
        dfDictionary[word] = int(dfDictionary.get(word, 0)) + 1



    #eyo this may take too long to go through the entire file. Do we just
    #get the JuLiDoTheThing dict??????????????????? eyoeyo
    for line in tokenByDocFreq:
        line = str(line)

        # If the word is in the line, extract the doc numbers and freqs.
        if word in line:
            line = line.strip()
            line = line.split(", ", 1)
            line[1] = line[1][2:len(line[1])-2]
            tempList = line[1].split("], [")

            # Go through each doc number that that the word is in
            # and save the doc num, word, and word frequency in that doc in a dict.
            # This is done through the use of a dictionary where the doc num
            # is the key and the word and word freq is a list in a list.
            for item in tempList:
                item = item.split(", ")
                docNum = int(item[0])
                docFreq = int(item[1])

                # If there is already an entry for that doc, add the word
                # and its corresponding doc freq as the value. Otherwise,
                # initialize the dictionary entry. For each doc
                # number, save the word found in it and that word's doc
                # frequency. EYO is this even right tho
                if (DocsThatContainQueryWords.get(docNum, False) != False):
                    tempoList = DocsThatContainQueryWords[docNum]

                    tempoList.append([word, docFreq])
                    DocsThatContainQueryWords[docNum] = tempoList
                else:
                    tempoList = list()
                    tempoList.append([word, docFreq])
                    DocsThatContainQueryWords[docNum] = tempoList

                # Add to the total count of times a word is in a doc.
                dfDictionary[word] = int(dfDictionary.get(word, 0)) + 1



# Find the tf idf for each word in the query.
for word,count in QueryWords.items():

    # Calculate the tf for the word, which is the count of that word in the
    # query over the maximum frequency of a certain word in the query.
    tf = count / maxFreq

    # The number of documents containing this word.
    df = dfDictionary[word]

    # The log of the total number of docs over the number of docs that this
    # word is in. Use laplace smoothing (+ 1) to compensate for 0 values.
    idf = math.log10(countOfDocs/df) + 1

    # Save the word's idf.
    QueryIdf[word] = idf

    # Calculate the tfidf.
    tfidf = tf*idf

    # Set the tfidf for each word into a dictionary. This is the word's weight.
    QueryTfIdf[word] = tfidf

    # Get the total for ||Query||  to be used when finding Cosine Similarity
    QueryNumForCosine = QueryNumForCosine + math.sqrt(tfidf ** 2)


# Find the tf idf for each word in their documents.
for doc,val in DocsThatContainQueryWords.items():

    # TODO: heyo casie, you need to do this
    # To accumulate a total score for each retrieved document, store retrieved
    # documents in a hashtable (or another search data structure),
    # where the document id is the key, and the partial accumulated score is
    # the value.


    # Initialize a dictionary that will contain all query words in the
    # document and how many times they appear.
    TemporaryWordDict = dict()

    # Initialize a dictionary to be used to save the tfidf for each doc's  query
    # words that appears in it. This saves the final tfidf value to be used in
    # the dot product and cosine similarity.
    DocAndWordTfIdf = dict()


    # Extract the query words found in the document and their respective counts.
    for item in val:
        item = item.split(", ")
        word = int(item[0])
        docFreq = int(item[1])
        TemporaryWordDict[word] = docFreq

    # Find the highest frequency value of a query value in the document
    # Eyo does this work tho

    maxDocFreq = max(TemporaryWordDict, key=lambda i: TemporaryWordDict[i])

    # Go through each of the query words found in this doc.
    for word,freq in TemporaryWordDict.items():

        # Calculate the tf for the word, which is the count of that word in the
        # doc over the maximum frequency of query words in the doc.
        tf = freq / maxDocFreq

        # Should we put laplace smoothing here? eyo

        # Get that word's idf. Eyo confirm that this is how you calculate this?
        idf = QueryIdf[word]

        # Calculate the tfidf.
        tfidf = tf*idf


        # Set the tfidf for each word into a dictionary. This is the doc's weight...???
        DocAndWordTfIdf[word] = tfidf

        # Get the total for ||Document #|| to be used when finding Cosine Similarity
        DocNumForCosine = DocNumForCosine + math.sqrt(tfidf ** 2)

    # Call the function that calculates the cosine similarity. Set the returned
    # value (the document's cosine similarity) as the value for that doc in the
    # dictionary.
    cosineSim = findCosineSim(DocAndWordTfIdf,QueryTfIdf,DocNumForCosine,QueryNumForCosine)
    cosineSimDict[doc] = cosineSim



#eyo I struggle with global variables.... does this know the dictionaries?
def findCosineSim(DocAndWordTfIdf,QueryTfIdf,DocNumForCosine,QueryNumForCosine):
    dotProduct = 0

    # Go through the document's query words, extracting each query word's tfidf
    # and each document word's tfidf. Multiply both values and add them to the
    # overall total of dot product.

    #EYO CASIE!! NO!! THERE IS A DIFF DOT PRODUCT FOR EVERY  DOCUMENT
    for word,tfidf in DocAndWordTfIdf.items():
        docWordTfidf = tfidf
        queryWordTfidf = QueryTfIdf[word]
        dotProduct = dotProduct + (docWordTfidf * queryWordTfidf)

    # Calculate the cosine similarity by dividing the Dot Product with the
    # product of the ||Document #|| and ||Query|| values.
    cosineSim = dotProduct/(DocNumForCosine * QueryNumForCosine)
    return cosineSim
