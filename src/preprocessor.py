import os
import re
from nltk.stem import PorterStemmer
import json
from pathlib import Path

# Builds and Store Inverted and Positional Index from Collection of Documents

class Preprocessor:
    def __init__(self,FolderName=None):
        self.docs = []                             #Document List
        self.PositonalIndex = {}                   
        self.dictionary = {}                       #Vocablary
        self.postings = {}                         #Posting List
        self.noOfDocs = 0                          
        self.stopwords = []
        self.CollectionDir = str(Path(__file__).parent.resolve()).replace('src',str(FolderName))   # Folder of Collection
        self.DataDir = str(Path(__file__).parent.resolve()).replace('src','data')                  # Folder to Store Indexes

    # Invokes function for building , storing and loading indexes

    def PreprocessingChain(self):

        if not os.path.isdir(self.DataDir):                #if directory already not present
            self.LoadStopwordsList()

            #creating indexes

            self.BuildInvertedIndex()
            self.BuildPositionalIndex()

            os.mkdir(self.DataDir)                          # creating data directory for storing and loading indexes

            # storing indexes

            self.WriteToDisk(self.docs,'Documents')
            self.WriteToDisk(self.dictionary,'Dictionary')
            self.WriteToDisk(self.postings,'Inverted_Index')
            self.WriteToDisk(self.PositonalIndex,'Positional_Index')

        else:
            
            #loading indexes from data directory

            self.docs = self.ReadFromDisk('Documents')
            self.noOfDocs = len(self.docs)                      #total documents in the collections
            self.dictionary = self.ReadFromDisk('Dictionary')
            self.postings = self.ReadFromDisk('Inverted_Index')
            self.PositonalIndex = self.ReadFromDisk('Positional_Index')

    def tokenize(self,text):
        text = text.lower()     #case folding
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

    # Stemmer - Porter Stemmer used

    def Stemming(self,token):
        ps = PorterStemmer()
        return ps.stem(token)   

    # Inverted Index Structure

    # Dictionary - key = Vocablary term  :  Value = list of docId in which term appears 
    
    # { "term1" : [docIDs] , "term2" : [docIds] , "term2" : [docIds], ..... , , "termN" : [docIds]}

    #Entire Index is build in single pass through the collection

    def BuildInvertedIndex(self):

        # files are not read from directory in sorted order, so reading files of a directory and sorting their names
        # reason - so that posting lists are sorted, sorted posting lists alllows intersection in linear time 

        files = os.listdir(self.CollectionDir)
        files = [int(x.replace('.txt','')) for x in files]
        files.sort()
        files = [ str(x)+'.txt' for x in files ]

        for filename in files:
            with open(os.path.join(self.CollectionDir, filename), 'r') as f:
                text = f.read()
                text_words = self.tokenize(text)
                self.docs.append(filename) 

                for word in text_words:
                    if not self.isStopword(word):                           #Stopwords Removal

                        word = self.Stemming(word)                          #Stemming

                        if word not in self.dictionary:
                        
                            self.postings[word] = [self.noOfDocs]           #initializing posting list
                            self.dictionary[word] = 1                       #initializing document count
                        
                        elif self.noOfDocs not in self.postings.get(word):
                        
                            self.postings[word].append(self.noOfDocs)       #appending posting list
                            self.dictionary[word] += 1                      #incrementing document count
                    
                self.noOfDocs+=1

    # Postional Index Structure

    # {Vocablary term : {"docId in which term appears" : [postions at which term appear in that document] } } 
    
    # { "term1" : { "docId1" : [postions] , "docId2" : [postions] } , "term2" : { "docId1" : [postions] , "docId2" : [postions] },
    #   .... "termN" : { "docId1" : [postions] , "docId2" : [postions] } }

    #Entire Index is build in single pass through the collection

    def BuildPositionalIndex(self):
        
        Dno = 0

        files = os.listdir(self.CollectionDir)
        files = [int(x.replace('.txt','')) for x in files]
        files.sort()
        files = [ str(x)+'.txt' for x in files ]

        for filename in files:
            with open(os.path.join(self.CollectionDir, filename), 'r') as f:
                text = f.read()
                text_words = self.tokenize(text)

                i=0         #for identifying postion of term in document

                for word in text_words:

                    if not self.isStopword(word):                           #filter out stopwords
                        
                        word = self.Stemming(word)                          #Stemming

                        if word not in [*self.PositonalIndex.keys()]:       #if term not present in the index 
                            self.PositonalIndex[word] = {Dno:[i]}           #initializing posting list
                        
                        elif Dno not in [*self.PositonalIndex[word].keys()]:   #if term appears first time in a document
                            self.PositonalIndex[word][Dno] = [i]               #appending posting list
                        
                        else:                                                  #if term has already appeared in the document
                            self.PositonalIndex[word][Dno].append(i)
                    i+=1

                Dno+=1
    
    #Writing Specified Index on Disk

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
