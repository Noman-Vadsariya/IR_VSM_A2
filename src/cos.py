from pre import Preprocessor
import re

class Ranking:

    def __init__(self):
        pass

    def process_query(self,query):

        p = Preprocessor()
        
        tokens = p.tokenize(query)
        
        print(tokens)

    # def ():




r = Ranking()
r.process_query('supervised kernel k-NN k-means cluster')
