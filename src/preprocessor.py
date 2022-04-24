import os
from pydoc import doc
import re
from nltk.stem import WordNetLemmatizer
import json
from pathlib import Path
import math

# Builds and Stores Term frequency index, Inverse document index and tfidf index from Collection of Documents
class Preprocessor:
    def __init__(self, FolderName=None):

        self.tf_index = {}          # term frequency index
        self.idf_index = {}         # inverse document frequency index
        self.tfidf_index = {}       # tfidf index

        self.noOfDocs = 0           # total document count

        self.stopwords = []         # stopword list

        self.CollectionDir = str(Path(__file__).parent.resolve()).replace("src", str(FolderName))  # Folder of Collection

        self.DataDir = str(Path(__file__).parent.resolve()).replace("src", "data")  # Folder to Store Indexes

    
    # Invokes function for building , storing and loading indexes
    def PreprocessingChain(self):

        # Storing and Loading Indexes
        
        if not os.path.isdir(self.DataDir):  # if directory already not present
            self.LoadStopwordsList()

            # creating indexes

            self.BuildTfIndex()
            self.length_normalization()
            self.BuildIdfIndex()
            self.BuildTfIdfIndex()

            # creating data directory for storing and loading indexes

            os.mkdir(self.DataDir)          
            self.WriteToDisk(self.tf_index, "tf_index")
            self.WriteToDisk(self.idf_index, "idf_index")
            self.WriteToDisk(self.tfidf_index, "tfidf_index")

        else:
            # loading indexes from data directory

            self.LoadStopwordsList()
            self.tf_index = self.ReadFromDisk("tf_index")
            self.idf_index = self.ReadFromDisk("idf_index")
            self.tfidf_index = self.ReadFromDisk("tfidf_index")
            self.noOfDocs = len(self.tf_index.keys())

    
    def tokenize(self, text):

        text = text.lower()                   # case folding
        text = re.sub(r"-", " ", text)        # handling hyphen
        text = re.sub(r"[^\w\s]", " ", text)  # noise removal - replacing all types of [^a-zA-Z0-9] and [^\t\r\n\f] with space for splitting on space
        text = text.split()                   # splitting on space
        return text

    
    # reading stopwords from stopwords file
    def LoadStopwordsList(self):

        pathToStopwords = str(Path(__file__).parent.resolve()).replace(
            "src", str("Stopwords")
        )

        for filename in os.listdir(pathToStopwords):

            with open(os.path.join(pathToStopwords, filename), "r") as f:
                self.stopwords += f.read().splitlines()

            f.close()

        while "" in self.stopwords:
            self.stopwords.remove("")

        self.stopwords = [x.replace(" ", "") for x in self.stopwords]   # removing extra endspaces

    
    # returns true if term present in stopwords list
    def isStopword(self, term):
        return term in self.stopwords

    
    # Lemmatization - WordNetLemmatizer used
    def Lemmatization(self, token):
        l = WordNetLemmatizer()
        return l.lemmatize(token)

    # for query parsing and preprocessing
    def FilterTokens(self, text):

        filteredList = []
        tokens = self.tokenize(text)
        for tok in tokens:
            if not self.isStopword(tok):
                tok = self.Lemmatization(tok)
                filteredList.append(tok)

        return filteredList


    # calculates term frequency for each unique term in each document.
    # tf_index = {doc1 : { t1 : 3, t2: 4, ... ,tn: 5}, doc1 : { t1 : 2, t2: 1, ... ,tn: 4}, ... , docN : { t1 : 1, t2: 4, ... ,tn: 2} )  
    
    def BuildTfIndex(self):

        # files are not read from directory in sorted order, so reading files of a directory and sorting their names
        # reason - so that posting lists are sorted, sorted posting lists alllows intersection in linear time

        files = os.listdir(self.CollectionDir)
        files = [int(x.replace(".txt", "")) for x in files]
        files.sort()
        files = [str(x) + ".txt" for x in files]

        docNo = 0

        for filename in files:

            with open(os.path.join(self.CollectionDir, filename), "r") as f:

                text = f.read()
                text_words = self.tokenize(text)

                for word in text_words:

                    if not self.isStopword(word):  # Stopwords Removal

                        word = self.Lemmatization(word)  # lemmatization

                        if docNo not in self.tf_index.keys():
                            self.tf_index[docNo] = {}               # adding term in a particular document

                        if word not in self.tf_index[docNo].keys():
                            self.tf_index[docNo][word] = 1          # initializing frequency count for a term
                        else:
                            self.tf_index[docNo][word] += 1         # incrementing frequency count for a term

            docNo += 1

        self.noOfDocs = docNo

    # Euclidean Normalization Vector / Magnitude of Vector => V / || V ||
    
    def length_normalization(self):

        self.magnitude = [0] * self.noOfDocs        # each index stores magnitude for a particular document

        for i in range(self.noOfDocs):

            for key in self.tf_index[i].keys():

                self.magnitude[i] += self.tf_index[i][key] ** 2

            self.magnitude[i] = math.sqrt(self.magnitude[i])        # sqrt(tf1^2 + tf2^2 + tf3^2 + ... + tfn^2)


    # calculates inverse document frequency  for each unique term
    # idf_index = { t1: idf-Val, t2: idf-Val , t3: idf-Val , ... , t4: idf-val }

    def BuildIdfIndex(self):
        df = {}

        for i in range(self.noOfDocs):
            temp = []
            for key in self.tf_index[i].keys():

                if key not in temp:
                    if key not in df.keys():
                        df[key] = 1
                    else:
                        df[key] += 1

                    temp.append(key)

        # idf will calculated for each unique term
        for k in df.keys():
            self.idf_index[k] = math.log10(self.noOfDocs / df[k])  # idf = log(N/df)


    # calculates tf*idf  for each unique term
    # tfidf_index = {doc1 : { t1 : 0.21, t2: 2.4, ... ,tn: 0.11}, doc1 : { t1 : 2.4, t2: 0.01, ... ,tn: 0.234}, ... , docN : { t1 : 0.21, t2: 0.344, ... ,tn: 0.2})
    
    def BuildTfIdfIndex(self):

        for i in range(self.noOfDocs):

            self.tfidf_index[str(i)] = {}

            for key in self.tf_index[i].keys():

                tf = (self.tf_index[i][key] / self.magnitude[i])    # length normalizing term frequency vector
                idf = self.idf_index[key]
                self.tfidf_index[str(i)][key] = tf * idf            # tfidf = tf * log(N/df)

   
    # writing specified index to disk

    def WriteToDisk(self, index, indexType):
        filename = "\\" + indexType + ".txt"
        with open(self.DataDir + filename, "w") as filehandle:
            filehandle.write(json.dumps(index))

    
    # reading specified Index from Disk

    def ReadFromDisk(self, indexType):
        filename = "\\" + indexType + ".txt"
        with open(self.DataDir + filename, "r") as filehandle:
            index = json.loads(filehandle.read())

        return index
