from .preprocessor import Preprocessor
# from pre import Preprocessor
import re
import math

#   takes query as input, preprocesses query , finds cosine similarity b/w query and every document in the collection
#   return top K document based on alpha
 
class Similarity:

    def process_query(self,query):

        p = Preprocessor('Abstracts')
        p.PreprocessingChain()
        tokens = p.FilterTokens(query)                  # proprocessing query

        query_tf_index = self.BuildTfVector(tokens)     # term frequency vector for query

        query_tfidf_index = self.BuildTfIdfVector(query_tf_index,p.idf_index)   # tfidf vector for query

        return self.CosineSimilarity(p.noOfDocs,p.tfidf_index,query_tfidf_index)  

    
    # calculate term frequency vector for query
    def BuildTfVector(self,tokens):

        query_tf_index = {}

        #   calculating frquency count for terms in query

        for tok in tokens:

            if tok not in query_tf_index:
                query_tf_index[tok] = 1
            else:
                query_tf_index[tok] += 1


        #   calculating magnitude of query vector

        magnitude = 0
        for k in query_tf_index.keys():
            magnitude += query_tf_index[k] ** 2

        magnitude = math.sqrt(magnitude)    #   sqrt(tf1^2 + tf2^2 + tf3^2 + ... + tfn^2)

        #   length normalizing term frequency vector query
        
        for k in query_tf_index:
            query_tf_index[k] = query_tf_index[k] / magnitude

        return query_tf_index
    

    #   calculating tfidf for query
    def BuildTfIdfVector(self,query_tf_index,idf_index):
        
        query_tfidf_index = {}

        for key in query_tf_index:

            idf = idf_index[key]
            tf = query_tf_index[key]
            query_tfidf_index[key] = tf * idf

        return query_tfidf_index
            

    # finds cosine similarity b/w query and every document in the collection

    def CosineSimilarity(self,noOfDocs,docs_tfidf_index,query_tfidf_index):
        
        sim_score = {}

        # Since we have normalized term freqeuncy = Dot Product
        # cosine_sim(d,q) = (d . q) /  || d || . || q || =  d . q

        for i in range(noOfDocs):

            for key in query_tfidf_index.keys():
            
                if key in docs_tfidf_index[str(i)].keys():
                    
                    if i not in sim_score.keys():
                        sim_score[i] = 0

                    sim_score[i] += (query_tfidf_index[key] * docs_tfidf_index[str(i)][key])


        # filtering based on alpha = 0.001

        result = []

        for key in sim_score.keys():
            if sim_score[key] >= 0.001:
                result.append(key)

        result = [x+1 for x in result]
        result.sort()       # displaying in numerical order, as in gold query set
        return result
