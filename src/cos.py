# from .pre import Preprocessor
from pre import Preprocessor
import re
import math

class Ranking:

    def __init__(self):
        pass

    def process_query(self,query):

        p = Preprocessor('Abstracts')
        p.PreprocessingChain()
        tokens = p.FilterTokens(query)

        query_tf_index = self.BuildTfVector(tokens)
        query_tfidf_index = self.BuildTfIdfVector(query_tf_index,p.idf_index)

        # TODO:  DOC count
        return self.CosineSimilarity(448,p.tfidf_index,p.doc_magnitudes,query_tfidf_index)

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
            # query_tf_index[key] = query_tf_index[key]
            query_tf_index[key] = query_tf_index[key]/df
            
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
            
    def CosineSimilarity(self,total_docs,docs_tfidf_index,doc_magnitudes,query_tfidf_index):
        sim_score = {}
        mag_query = 0.0

        # print(query_tfidf_index)

        for key in query_tfidf_index.keys():
            print(key)

            mag_query += query_tfidf_index[key]**2

            keys = list(map(int, [*docs_tfidf_index[key].keys()]))
            
            # print(keys)

            for i in range(total_docs):
                
                if i in keys:
                    # print(sim_score.keys())
                    if i not in sim_score.keys():
                        sim_score[i] = 0

                    sim_score[i] += docs_tfidf_index[key][str(i)] * query_tfidf_index[key]

        # cosine_sim(d,q) = (d . q) /  || d || . || q ||
        print(math.sqrt(mag_query))

        print(doc_magnitudes)        
        
        print()

        print(sim_score)

        for i in sim_score.keys():
            sim_score[i] = sim_score[i] / ( doc_magnitudes[str(i)] * math.sqrt(mag_query) )

        print()

        print(sim_score)

        # sim_score = dict(sorted(sim_score.items(), key=lambda x:x[1],reverse=True))

        print()

        result = []

        for key in sim_score.keys():
            if sim_score[key] >= 0.001:
                result.append(key)

        print(result)

        result = [x+1 for x in result]
        result.sort()
        print(result)
        return result


r = Ranking()
# r.process_query('deep')
# r.process_query('weak heuristic')
# r.process_query('principle component analysis')
# r.process_query('human interaction')
r.process_query('synergy analysis')
# r.process_query('github mashup apis')
# r.process_query('Bayesian nonparametric')
# r.process_query('diabetes and obesity')
# print(r.process_query('bootstrap'))
# r.process_query('ensemble')
# r.process_query('markov ')
# r.process_query('prioritize and critical correlate')
# print(r.process_query('local global clusters'))
# r.process_query('supervised kernel k-means cluster')

# print(r.process_query('w2 w5 w6'))
