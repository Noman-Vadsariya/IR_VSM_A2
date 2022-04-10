from .preprocessor import Preprocessor

# processes boolean query

class BooleanQuery:
    def __init__(self, Dictionary, Postings, totalDocs):
        self.Postings = Postings
        self.Dictionary = Dictionary
        self.totalDocs = totalDocs

    # returns documents in which term appears

    def get_posting(self, term):
        if term in [*self.Postings.keys()]:
            return self.Postings[term]
        else:
            print(term + " Not in Vocablary")
            return []

    # return Document Frequency for a term

    def get_posting_size(self, term):
        if term in [*self.Dictionary.keys()]:
            return self.Dictionary[term]
        else:
            print(term + " not in vocablary")
            return -1

    # performs intersection operation of two posting list

    def intersect(self, p1, p2):
        answer = []

        i1 = 0
        i2 = 0
        while i1 < len(p1) and i2 < len(p2):   # untill docId's of either t1 or t2 are not completely traversed
            
            if p1[i1] == p2[i2]:               # docId matches
                answer.append(p1[i1])
                i1 += 1
                i2 += 1

            elif p1[i1] < p2[i2]:
                i1 += 1
            else:
                i2 += 1

        return answer

    # performs union operation of two posting list

    def union(self, p1, p2):
        answer = []
        i1 = 0
        i2 = 0

        while i1 < len(p1) and i2 < len(p2):
            if p1[i1] == p2[i2]:
                answer.append(p1[i1])
                i1 += 1
                i2 += 1
            elif p1[i1] < p2[i2]:
                answer.append(p1[i1])
                i1 += 1
            else:
                answer.append(p2[i2])
                i2 += 1

        while i1 < len(p1):
            answer.append(p1[i1])
            i1 += 1

        while i2 < len(p2):
            answer.append(p2[i2])
            i2 += 1

        return answer

    # performs complement operation on given posting list

    def complement(self, p):
        answer = []
        for i in range(self.totalDocs):             #appending all docIds excepts the one in which term occurs 
            if i not in p:
                answer.append(i)

        return answer

    # Parses Boolean Query and Caculates Processing Cost
    
    def ProcessQuery(self, query):

        processingCost = 0  # no of DocIDs traversed

        p = Preprocessor()                               
        tokens = query.split()                      #split query

        for i in range(len(tokens)):                #stem query terms
            tokens[i] = p.Stemming(tokens[i])

        if (len(tokens)) == 1:                                           # if single term simple return posting list of term
            processingCost = 0
            tempResult = self.get_posting(tokens[0])

        elif (len(tokens)) == 2 and tokens[0].upper() == "NOT":          #if two terms then it will be NOT operation
            processingCost = self.totalDocs - self.get_posting_size(tokens[1])
            tempResult = self.complement(self.get_posting(tokens[1]))

        else:
            i = 0
            tempResult = None

            #linearly traversing query terms and perform operator left to right
            
            while i < len(tokens):

                if tokens[i].upper() == "AND":
                    if tempResult is None:
                        if i - 2 >= 0 and tokens[i - 2] == "NOT":
                            p1 = self.complement(self.get_posting(tokens[i - 1]))
                        else:
                            p1 = self.get_posting(tokens[i - 1])

                    if tokens[i + 1] == "NOT" and i + 2 < len(tokens):
                        p2 = self.complement(self.get_posting(tokens[i + 2]))
                        i += 2
                    else:
                        p2 = self.get_posting(tokens[i + 1])
                        i += 1

                    if tempResult is None:
                        tempResult = p1

                    processingCost += min(len(tempResult), len(p2))
                    tempResult = self.intersect(tempResult, p2)

                elif tokens[i].upper() == "OR":
                    if tempResult is None:
                        if i - 2 >= 0 and tokens[i - 2] == "NOT":
                            p1 = self.complement(self.get_posting(tokens[i - 1]))
                        else:
                            p1 = self.get_posting(tokens[i - 1])

                    if tokens[i + 1] == "NOT" and i + 2 < len(tokens):
                        p2 = self.complement(self.get_posting(tokens[i + 2]))
                        i += 2
                    else:
                        p2 = self.get_posting(tokens[i + 1])
                        i += 1

                    if tempResult is None:
                        tempResult = p1

                    processingCost += len(tempResult) + len(p2)
                    tempResult = self.union(tempResult, p2)   # cost of union operation can be at min will be 0
                i += 1

        result = [i + 1 for i in tempResult]
        return (result, processingCost)
