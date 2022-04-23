import os
from pydoc import doc
import re
from nltk.stem import WordNetLemmatizer
import json
from pathlib import Path
import math

# Builds and Store Inverted and Positional Index from Collection of Documents

class Preprocessor:
    def __init__(self,FolderName=None):
        self.docs = []                             #Document List
        self.tf_index = {}                   
        self.idf_index = {}                   
        self.tfidf_index = {}                   
        self.dictionary = {}                       #Vocablary
        self.noOfDocs = 0                          
        self.stopwords = []
        self.CollectionDir = str(Path(__file__).parent.resolve()).replace('src',str(FolderName))   # Folder of Collection
        self.DataDir = str(Path(__file__).parent.resolve()).replace('src','data')                  # Folder to Store Indexes

    # Invokes function for building , storing and loading indexes

    def PreprocessingChain(self):
        
        if not os.path.isdir(self.DataDir):                #if directory already not present
            self.LoadStopwordsList()

            #creating indexes
            self.BuildTfIndex()
            self.BuildIdfIndex()
            self.BuildTfIdfIndex()

            os.mkdir(self.DataDir)                          # creating data directory for storing and loading indexes

            # storing indexes

            # self.WriteToDisk(self.docs,'Documents')
            self.WriteToDisk(self.tf_index,'tf_index')
            self.WriteToDisk(self.idf_index,'idf_index')
            self.WriteToDisk(self.tfidf_index,'tfidf_index')
            # self.WriteToDisk(self.dictionary,'Dictionary')

        else:
            
            #loading indexes from data directory

            # self.docs = self.ReadFromDisk('Documents')
            self.tf_index = self.ReadFromDisk('tf_index')
            self.idf_index = self.ReadFromDisk('idf_index')
            self.tfidf_index = self.ReadFromDisk('tfidf_index')
            self.LoadStopwordsList()

    def tokenize(self,text):
        text = text.lower()     #case folding
        # text = re.sub(r'-','',text)  # handling hyphen 
        text = re.sub(r'-',' ',text)  # handling hyphen 
        text = re.sub(r'[^\w\s]',' ',text)   #noise removal - replacing all types of [^a-zA-Z0-9] and [^\t\r\n\f] with space for splitting on space
        text = text.split()     #splitting on space
        return text

    # reading stopwords from stopword file

    def LoadStopwordsList(self):
        pathToStopwords = str(Path(__file__).parent.resolve()).replace('src',str('Stopwords'))
        for filename in os.listdir(pathToStopwords):
            with open(os.path.join(pathToStopwords, filename), 'r') as f:
                self.stopwords += f.read().splitlines()

            f.close()

        while '' in self.stopwords: self.stopwords.remove('')
        self.stopwords = [x.replace(' ','') for x in self.stopwords]

    # returns true if term present in stopwords list

    def isStopword(self,term):
        return term in self.stopwords

    # Lemmatization - WordNetLemmatizer used

    def Lemmatization(self,token):
        l = WordNetLemmatizer()
        return l.lemmatize(token)   

    def FilterTokens(self,text):
        
        filteredList = []
        tokens = self.tokenize(text)
        for tok in tokens:
            if not self.isStopword(tok):
                tok = self.Lemmatization(tok)
                filteredList.append(tok)

        return filteredList

    def BuildTfIndex(self):
        
        # files are not read from directory in sorted order, so reading files of a directory and sorting their names
        # reason - so that posting lists are sorted, sorted posting lists alllows intersection in linear time 

        files = os.listdir(self.CollectionDir)
        files = [int(x.replace('.txt','')) for x in files]
        files.sort()
        files = [ str(x)+'.txt' for x in files ]

        totalDocs = len(files)
        docNo = 0

        for filename in files:
            
            with open(os.path.join(self.CollectionDir, filename), 'r') as f:
                
                text = f.read()
                text_words = self.tokenize(text)
                self.docs.append(filename) 

                for word in text_words:

                    if not self.isStopword(word):                           #Stopwords Removal

                        word = self.Lemmatization(word)                          #lemmatization

                        if word not in self.tf_index.keys():
                        
                            self.tf_index[word] = {docNo:1}           #initializing posting list
                        
                        elif docNo not in self.tf_index[word].keys():

                            self.tf_index[word][docNo] = 1
                        
                        else:

                            self.tf_index[word][docNo] += 1

                self.noOfDocs+=1

            docNo += 1
                
        # print(self.tf_index)
        # self.WriteToDisk(self.tf_index,'tf_index')

    # df = No of Docs in which term appears
    def BuildIdfIndex(self):
        
        # print(self.noOfDocs)
        # print(self.tf_index.keys())

        for word in self.tf_index.keys():

            df = len(self.tf_index[word].keys())

            idf = math.log10( self.noOfDocs / df )
            # idf = math.log10(df)/self.noOfDocs

            self.idf_index[word] = idf

        # print(self.idf_index)
        # self.WriteToDisk(self.idf_index,'idf_index')


    def BuildTfIdfIndex(self):
        
        for word in self.tf_index.keys():

            self.tfidf_index[word] = {}

            for docNo in self.tf_index[word].keys():
                
                # tf = 1 + math.log10(self.tf_index[word][docNo])     # tf = 1 + log(tf)
                tf = math.log10(1+self.tf_index[word][docNo])     # tf = log(1+tf)
                # tf = self.tf_index[word][docNo]     # tf = tf / docFreq
                idf = self.idf_index[word]
                self.tfidf_index[word][docNo] = tf * idf
        
        # self.WriteToDisk(self.tfidf_index,'tfidf_index')


    def WriteToDisk(self,index,indexType):
        filename = '\\' + indexType + ".txt"
        with open(self.DataDir + filename, 'w') as filehandle:
            filehandle.write(json.dumps(index))

    #reading Specified Index from Disk

    def ReadFromDisk(self,indexType):
        filename = '\\' + indexType + ".txt"
        with open(self.DataDir + filename, 'r') as filehandle:
            index = json.loads(filehandle.read())

        return index

p = Preprocessor('Abstracts')
p.PreprocessingChain()