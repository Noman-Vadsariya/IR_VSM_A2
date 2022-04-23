# from .pre import Preprocessor
from pre import Preprocessor
import re
import math

class Ranking:

    def __init__(self):
        pass

    def process_query(self,query):

        p = Preprocessor('Abstract')
        p.PreprocessingChain()
        tokens = p.FilterTokens(query)

        query_tf_index = self.BuildTfVector(tokens)
        query_tfidf_index = self.BuildTfIdfVector(query_tf_index,p.idf_index)

        # TODO:  DOC count
        return self.CosineSimilarity(448,p.tfidf_index,query_tfidf_index)

    def BuildTfVector(self,tokens):

        query_tf_index = {}

        for tok in tokens:

            if tok not in query_tf_index:
                query_tf_index[tok] = 1
            else:
                query_tf_index[tok] += 1

        print(query_tf_index)

        df = len(tokens)
        for key in query_tf_index.keys():

            # query_tf_index[key] = 1 + math.log10(query_tf_index[key])
            # query_tf_index[key] = math.log10(1+query_tf_index[key])
            query_tf_index[key] = query_tf_index[key]
            # query_tf_index[key] = query_tf_index[key]/df
            
        print(query_tf_index)
        return query_tf_index
    
    def BuildTfIdfVector(self,query_tf_index,idf_index):
        
        query_tfidf_index = {}

        for key in query_tf_index:

            idf = idf_index[key]
            tf = query_tf_index[key]
            query_tfidf_index[key] = tf * idf

        print(query_tfidf_index)
        return query_tfidf_index
            
    def CosineSimilarity(self,total_docs,docs_tfidf_index,query_tfidf_index):
        sim_score = {}
        mag_doc = {}
        mag_query = 0.0

        # print(query_tfidf_index)

        for key in query_tfidf_index.keys():
            print(key)

            mag_query += query_tfidf_index[key]**2

            keys = list(map(int, [*docs_tfidf_index[key].keys()]))
            
            # print(keys)

            for i in range(total_docs):
                
                if i in keys:
                    
                    if i not in sim_score.keys():
                        sim_score[i] = 0
                        mag_doc[i] = 0

                    if i == 0:
                        print(docs_tfidf_index[key][str(i)])
                    sim_score[i] += docs_tfidf_index[key][str(i)] * query_tfidf_index[key]
                    mag_doc[i] += docs_tfidf_index[key][str(i)]**2

        # cosine_sim(d,q) = (d . q) /  || d || . || q ||
        print(math.sqrt(mag_query))
        # print()
        print(mag_doc)
        # print(sim_score)

        for i in sim_score.keys():
            # print(math.sqrt(mag_doc[i]))
            sim_score[i] = sim_score[i] / (math.sqrt(mag_doc[i]) * math.sqrt(mag_query))

        result = []

        for key in sim_score.keys():
            if sim_score[key] >= 0.001:
                result.append(key)


        result = [x+1 for x in result]
        result.sort()
        return result


r = Ranking()
# r.process_query('deep')
# r.process_query('weak heuristic')
# r.process_query('principle component analysis')
# r.process_query('human interaction')
# print(r.process_query('bootstrap'))
# r.process_query('diabetes and obesity')
# r.process_query('github mashup apis')
# r.process_query('prioritize and critical correlate')
# print(r.process_query('local global clusters'))
# r.process_query('supervised kernel k-means cluster')

print(r.process_query('w2 w5 w6'))
