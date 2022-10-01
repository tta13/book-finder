import os

#import numpy as np
import math

from search_engine.inverted_index import (create_doc_ids, load_doc_ids, save_doc_ids, 
    save_field_inv_index, save_inv_index, load_field_inv_index, load_inv_index,
    count_frequent_fields, DATA_PATH)

def main():
    try:
        doc_ids = load_doc_ids(os.path.join(DATA_PATH, 'docIDs.json'))
    except Exception:
        save_doc_ids(create_doc_ids())

    try:
        # Loading inverted indexes
        field_index = load_field_inv_index()
        index = load_inv_index()
    except Exception:
        # Saving the inverted indexes then loading files
        save_field_inv_index(doc_ids)
        save_inv_index(doc_ids)
        field_index = load_field_inv_index()
        index = load_inv_index()

    field_lengt = get_documents_field_lengt(field_index)
    lengt = get_documents_lengt(index)

    tabletfidf = create_tfidf_table(index)
    tableIndextfidf = create_tfidf_index_table(field_index)

    scored = cosineScore(tabletfidf,index, lengt)

    print(scored)

    print("\n\n\n\n")
    scored = cosineScoreField(tableIndextfidf,field_index, field_lengt)

    print(scored)

def findtermtfidf(terms, term: str):
    N = len(terms)
    ni = 0
    for i in terms:
        if(i == term):
            ni+=1

    print(term)
    print(terms)
    print(ni)
    print(math.log2(N/ni))
    print((ni * math.log2(N/ni)))
    print("\n\n")

    return (ni * math.log2(N/ni))

def create_tfidf_table(index):
    tfidf_table = {}
    N = 7651 # size of doc_ids
    for key in index.vocab:

        idf = math.log2(N/len(index.search_term(key)))
        lista_gamb = []

        for tuplas in index.search_term(key):
            lista_gamb.append((tuplas[0],tuplas[1] * idf))

        tfidf_table[key] = lista_gamb
    
    return tfidf_table

def create_tfidf_index_table(field_index): # VER COM TALES SE N SE MANTÉM ENTRE INDEX_FIELD E INDEX NORMAL
    tfidf_table_fields = {}
    N = 7651 # size of doc_ids
    for key in field_index.vocab:

        idf = math.log2(N/len(field_index.search_term(key)))
        lista_gamb = []

        for tuplas in field_index.search_term(key):
            lista_gamb.append((tuplas[0],tuplas[1] * idf))

        tfidf_table_fields[key] = lista_gamb

    return tfidf_table_fields

def cosineScore(tfidf_table, index, lenght):
    terms = ["karl","marx"]

    scores = {}
    listofdocs = []

    for term in terms:
        if term in tfidf_table:
            term_tfidf = findtermtfidf(terms, term)

            for doc, score in tfidf_table[term]:
                if doc not in scores:
                    scores[doc] = score * term_tfidf #score = tfidf de um doc especifico / term tfidf = tfidf de um termo na query scores[doc] = document_term_tfidf * query_term_tfidf
                else:
                    scores[doc] += score * term_tfidf
                
                if doc not in listofdocs:
                    listofdocs.append(doc)
        
    for doc in listofdocs:
        scores[doc] = scores[doc]/ lenght[doc]

    scores = {item[0]: item[1]
              for item in sorted(scores.items(), key=lambda x: -x[1])}

    return scores

def cosineScoreField(tableIndextfidf, field_index, lenght):
    terms = ["karl.author","marx.author"]

    scores = {}
    listofdocs = []

    for term in terms:
        if term in tableIndextfidf:
            term_tfidf = findtermtfidf(terms, term)

            for doc, score in tableIndextfidf[term]:
                if doc not in scores:
                    scores[doc] = score * term_tfidf #score = tfidf de um doc especifico / term tfidf = tfidf de um termo na query scores[doc] = document_term_tfidf * query_term_tfidf
                else:
                    scores[doc] += score * term_tfidf
                
                if doc not in listofdocs:
                    listofdocs.append(doc)
        
    for doc in listofdocs:
        scores[doc] = scores[doc]/ lenght[doc]

    scores = {item[0]: item[1]
              for item in sorted(scores.items(), key=lambda x: -x[1])}

    return scores

def get_documents_lengt(index):
    lenght = {}

    for key in index.vocab:
        tmpposting = index.search_term(key)
        for tupla in tmpposting:
            if tupla[0] not in lenght:
                lenght[tupla[0]] = tupla[1]
            else:
                lenght[tupla[0]] += tupla[1]

    return lenght

def get_documents_field_lengt(field_index):
    lenght = {}

    for key in field_index.vocab:
        tmpposting = field_index.search_term(key)
        for tupla in tmpposting:
            if tupla[0] not in lenght:
                lenght[tupla[0]] = tupla[1]
            else:
                lenght[tupla[0]] += tupla[1]


    return lenght


if __name__ == '__main__':
    main()
