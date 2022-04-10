import os
import re
from .preprocessor import Preprocessor

#processes proximity query

class ProximityQuery:

    def __init__(self, PositionalIndex):
        self.PostionalIndex = PositionalIndex

    # returns documents in which term appears
    
    def get_posting(self, term):
        if term in [*self.PostionalIndex.keys()]:
            return self.PostionalIndex.get(term)
        else:
            print(term + " Not in Vocablary")
            return None

    # returns postions of a term within a document

    def get_positions(self, term, docID):
        return self.PostionalIndex[term][docID]


    def posting_intersect(self, t1, t2, k):

        answer = []

        #fetching postional posting list
        p1 = self.get_posting(t1)                       
        p2 = self.get_posting(t2)

        if p1 == None or p2 == None:                    #p1 or p2 == None - means term not in vocablary
            return []                                   #if either of the term is not in vocablary there can't be any intersection
            
        #getting docIds for each term
        p1 = list(p1.keys())                            
        p2 = list(p2.keys())

        i = 0
        j = 0
        while i < len(p1) and j < len(p2):              # untill docId's of either t1 or t2 are not completely traversed
            
            if int(p1[i]) == int(p2[j]):
               
                l = []              

                #getting index of term within a document
                pos1 = self.get_positions(t1, p1[i])     
                pos2 = self.get_positions(t2, p2[j])

                indexPos1 = 0
                indexPos2 = 0
                while indexPos1 != len(pos1):                              # while pos1 is not None
                    while indexPos2 != len(pos2):                          # while pos2 is not None
                        
                        if abs(pos1[indexPos1] - pos2[indexPos2]) <= k + 1:       # if word difference b/w two terms is <= proximity 
                            l.append(pos2[indexPos2])  
                        
                        elif pos2[indexPos2] > pos1[indexPos1]:  
                            break

                        indexPos2 += 1                    # next position of t2 in pos2
                    
                    while l != [] and abs(l[0] - pos1[indexPos1]) > k + 1:  
                        l.remove(l[0])  
                    
                    for ps in l:
                        answer.append([p1[i], pos1[indexPos1], ps])        # add answer(docID(p1), pos(pos1), ps)
                    
                    indexPos1 += 1        # next position of t1 in pos1
                
                i += 1        # next document for p1
                j += 1        # next document for p2

            elif int(p1[i]) < int(p2[j]):  # else if (docID(p1) < docID(p2))
                i += 1         # next document for t1
            else:   
                j += 1         # next document for t2 

        return answer

    #Parse Proximity Query of the form -> feature tracking /2

    def ProcessProximityQuery(self, query):
        
        tokens = query.split()      
        
        p = Preprocessor()

        #stemming input terms
        t1 = p.Stemming(tokens[0])                             
        t2 = p.Stemming(tokens[1])

        k = int(re.sub(r"[^\w\s]", "", tokens[2]))             #extract value of K

        result_set = self.posting_intersect(t1, t2, k)

        ret_docs = {}
        for result in result_set:
            docNo = int(result[0]) + 1                          # docNo = doc_index + 1
            if docNo not in ret_docs:
                ret_docs[docNo] = [(result[1], result[2])]
            else:
                ret_docs[docNo].append((result[1], result[2]))

        return ret_docs

