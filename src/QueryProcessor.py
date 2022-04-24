from .cosineSimilarity import Similarity

# Receives Query from frontend and responds with a resultset

class QueryProcessor():
    
    def __init__(self):
        pass

    def ProcessQuery(self,query):
        if query != "":
                
            try:
                processingCost = 0
                s = Similarity()
                result_set = s.process_query(query)
            except:
                return ["error",query]

            print(result_set)
            return (result_set,processingCost,query)
