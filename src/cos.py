# from .pre import Preprocessor
from pre import Preprocessor
import re
import math

class Ranking:

    def __init__(self):
        pass

    def process_query(self,query):

        p = Preprocessor('Abstracts')
        # p = Preprocessor('sample')
        p.PreprocessingChain()
        tokens = p.FilterTokens(query)

        query_tf_index = self.BuildTfVector(tokens)
        query_tfidf_index = self.BuildTfIdfVector(query_tf_index,p.idf_index)

        # TODO:  DOC count
        return self.CosineSimilarity(p.documents,p.tfidf_index,p.doc_magnitudes,query_tfidf_index)

    def BuildTfVector(self,tokens):

        query_tf_index = {}

        for tok in tokens:

            if tok not in query_tf_index:
                query_tf_index[tok] = 1
            else:
                query_tf_index[tok] += 1

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
            
    def CosineSimilarity(self,doc_length,docs_tfidf_index,doc_magnitudes,query_tfidf_index):
        sim_score = {}
        mag_query = 0.0

        # print(query_tfidf_index)

        for key in query_tfidf_index.keys():
            print(key)

            mag_query += query_tfidf_index[key]**2

            keys = list(map(int, [*docs_tfidf_index[key].keys()]))
            
            # print(keys)

            for i in range(len(doc_length)):
                
                if i in keys:
                    # print(sim_score.keys())
                    if i not in sim_score.keys():
                        sim_score[i] = 0

                    sim_score[i] += docs_tfidf_index[key][str(i)] * query_tfidf_index[key]

        # cosine_sim(d,q) = (d . q) /  || d || . || q ||
        # print(math.sqrt(mag_query))

        # print(doc_magnitudes)        
        
        # print()

        print(sim_score)
        maxScore = max(sim_score.values())
        print(maxScore)

        for i in sim_score.keys():
            if doc_magnitudes[str(i)] != 0 and math.sqrt(mag_query) !=0 :
                sim_score[i] = sim_score[i] / ( doc_magnitudes[str(i)] * math.sqrt(mag_query) )
            else:
                sim_score[i] = 0
            # sim_score[i] = sim_score[i] / doc_length[str(i)]  # length normalizing
            # sim_score[i] = sim_score[i] / maxScore  # length normalizing


        print()


        sim_score = dict(sorted(sim_score.items(), key=lambda x:x[1],reverse=True))

        # print(sim_score)
        print()

        result = []

        for key in sim_score.keys():
            if sim_score[key] >= 0.001:
                result.append(key)

        # print(result)

        result = [x+1 for x in result]
        result.sort()
        print(result)
        return result


r = Ranking()
# r.process_query('deep')
# r.process_query('weak heuristic')
# r.process_query('principle component analysis')
# r.process_query('human interaction')
# r.process_query('supervised kernel k-means cluster')
# r.process_query('patients depression anxiety')
# r.process_query('local global clusters')
# r.process_query('synergy analysis')
# r.process_query('github mashup apis')
# r.process_query('Bayesian nonparametric')
# r.process_query('diabetes and obesity')
# print(r.process_query('bootstrap'))
# r.process_query('ensemble')
# r.process_query('markov ')
r.process_query('prioritize and critical correlate')

# print(r.process_query('w1 w2 w1'))
