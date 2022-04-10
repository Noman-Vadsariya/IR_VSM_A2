# IR_VSM_A2

#Preprocessing chain

    parse document
    
    stopword removal

    lemmatization

    Build TF index
    
    Build IDF index
    
    Build TF-IDF Index

    Store All three indexes

#Query Time - Run Time Processing

    parse query
    
    calculate TF vector for query -> simple dictionary {term : tf}
    
    calculate TF-IDF for query -> simple dictionary {term : TF-IDF}

    calculate cosine similarity of query and each document(488)
    
        optimization - only multiply tf-idf of term common in query and document

    filter documents based on alpha=0.0001

