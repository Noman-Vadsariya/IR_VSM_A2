from .cos import Ranking

# Receives Query from frontend and responds with a resultset

class QueryProcessor():
    
    def __init__(self):
        pass

    def ProcessQuery(self,query):
        if query != "":
                
            try:
                processingCost = 0
                r = Ranking()
                result_set = r.process_query(query)
            except:
                return ["error",query]

            print(result_set)
            return (result_set,processingCost,query)
