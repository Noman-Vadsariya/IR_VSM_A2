from .preprocessor import Preprocessor
from .booleanQuery import BooleanQuery
from .proximityQuery import ProximityQuery

# Receives Query from frontend and responds with a resultset

class QueryProcessor():
    
    def __init__(self):
        pass

    def ProcessQuery(self,query):
        if query != "":
                p = Preprocessor("Abstracts")
                p.PreprocessingChain()
                tokens = query.split()
                processingCost = -1
                try:
                    if len(tokens)>2 and '/' == tokens[2][0]:     # if / present, then proximity query else boolean query
                        prox = ProximityQuery(p.PositonalIndex)
                        result_set = prox.ProcessProximityQuery(query)
                    else:
                        b = BooleanQuery(p.dictionary, p.postings, p.noOfDocs)
                        result_set,processingCost = b.ProcessQuery(query)
                except:
                    return ["error",query]

                print(result_set)
                return (result_set,processingCost,query)
