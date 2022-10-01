import os

#import numpy as np
import math
import scipy.stats as stats

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

    #scored = cosineScore(tabletfidf,index, lengt, terms)
    #scored = cosineScoreField(tableIndextfidf,field_index, field_lengt, terms)
    #scored = cosineScoreTF(index, lengt, terms)
    #scored = cosineScoreFieldTF(field_index, field_lengt, terms)

    print("\n\n\n\n")

    termsfield = ["karl.author","marx.author"]
    terms = ["karl","marx"]

    scored1 = cosineScoreFieldTF(field_index, field_lengt, termsfield)
    #print(scored1)

    print("\n\n\n\n")
    scored2 = cosineScoreTF(index, lengt, terms)
    #print(scored2)

    print("\n\n\n\n")
    scored3 = cosineScore(tabletfidf,index, lengt, terms)
    #print(scored3)

    print("\n\n\n\n")
    scored4 = cosineScoreField(tableIndextfidf,field_index, field_lengt, termsfield)
    #print(scored4)

    print("\n\n\n\n")

    tau1 = get_kendal_tau(scored1,scored4)
    #tau2 = get_kendal_tau(scored1,scored2)
    #tau3 = get_kendal_tau(scored1,scored3)
    tau4 = get_kendal_tau(scored2,scored3)
    #tau5 = get_kendal_tau(scored2,scored4)
    #tau6 = get_kendal_tau(scored3,scored4)
    
    print(f'tau: {tau1}')
    
   
    print(f'tau: {tau4}')
    
def get_kendal_tau(dic1, dic2):
    list1 = []
    list2 = []
    for i in dic1.keys():
        list1.append(i)
    for i in dic2.keys():
        list2.append(i)

    pairs1 = []
    pairs2 = []
    for i in range(len(list1)):
        for j in range(i + 1, len(list1)):
            pairs1.append([list1[i], list1[j]])

    for i in range(len(list2)):
        for j in range(i + 1, len(list2)):
            pairs2.append([list2[i], list2[j]])

    if not len(list1) or not len(list2):
        return 0

    if len(list1) == 1 or len(list2) == 1:
        return 1 if list1[0] == list2[0] else 0

    concordant_pairs = 0
    for i in range(len(pairs1)):
        if pairs1[i] not in pairs2:
            concordant_pairs += 1

    concordant_pairs *= 2
    tal =  1 - 2 * concordant_pairs / (2 * len((pairs1)))

    tau, p_value = stats.kendalltau(list1, list2)

    print(f'tal: {tal}\n tau: {tau}\n')

    return tal

def findtermtfidf(terms, term: str):
    N = len(terms)
    ni = 0
    for i in terms:
        if(i == term):
            ni+=1

    return (ni * math.log2(N/ni))

def findtermtf(terms, term: str):
    N = len(terms)
    ni = 0
    for i in terms:
        if(i == term):
            ni+=1

    return (ni)

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

def create_tfidf_index_table(field_index):
    tfidf_table_fields = {}
    N = 7651 # size of doc_ids
    for key in field_index.vocab:

        idf = math.log2(N/len(field_index.search_term(key)))
        lista_gamb = []

        for tuplas in field_index.search_term(key):
            lista_gamb.append((tuplas[0],tuplas[1] * idf))

        tfidf_table_fields[key] = lista_gamb

    return tfidf_table_fields

def cosineScore(tfidf_table, index, lenght,terms):

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

def cosineScoreTF(index, lenght,terms):

    scores = {}
    listofdocs = []

    for term in terms:
        if term in index.vocab:
            term_tf = findtermtf(terms, term)
            tmptupla = index.search_term(term)

            for doc, score in tmptupla:
                if doc not in scores:
                    scores[doc] = score * term_tf #score = tfidf de um doc especifico / term tfidf = tfidf de um termo na query scores[doc] = document_term_tfidf * query_term_tfidf
                else:
                    scores[doc] += score * term_tf
                
                if doc not in listofdocs:
                    listofdocs.append(doc)
        
    for doc in listofdocs:
        scores[doc] = scores[doc]/ lenght[doc]

    scores = {item[0]: item[1]
              for item in sorted(scores.items(), key=lambda x: -x[1])}

    return scores


def cosineScoreField(tableIndextfidf, field_index, lenght, terms):
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

def cosineScoreFieldTF(field_index, lenght, terms):

    scores = {}
    listofdocs = []

    for term in terms:
        if term in field_index.vocab:
            term_tf = findtermtf(terms, term)
            tmptupla = field_index.search_term(term)

            for doc, score in tmptupla:
                if doc not in scores:
                    scores[doc] = score * term_tf #score = tfidf de um doc especifico / term tfidf = tfidf de um termo na query scores[doc] = document_term_tfidf * query_term_tfidf
                else:
                    scores[doc] += score * term_tf
                
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

def get_Query_Rank(terms):
    try:
        doc_ids = load_doc_ids(os.path.join(DATA_PATH, 'docIDs.json'))
    except Exception:
        save_doc_ids(create_doc_ids())

    try:
        # Loading inverted indexes
        index = load_inv_index()
    except Exception:
        # Saving the inverted indexes then loading files
        save_inv_index(doc_ids)
        index = load_inv_index()

    lengt = get_documents_lengt(index)

    tabletfidf = create_tfidf_table(index)

    return cosineScore(tabletfidf,index, lengt, terms)

def get_Query_Index_Rank(terms):
    try:
        doc_ids = load_doc_ids(os.path.join(DATA_PATH, 'docIDs.json'))
    except Exception:
        save_doc_ids(create_doc_ids())

    try:
        # Loading inverted indexes
        field_index = load_field_inv_index()
    except Exception:
        # Saving the inverted indexes then loading files
        save_field_inv_index(doc_ids)
        field_index = load_field_inv_index()

    field_lengt = get_documents_field_lengt(field_index)

    tableIndextfidf = create_tfidf_index_table(field_index)

    return cosineScoreField(tableIndextfidf,field_index, field_lengt, terms)


if __name__ == '__main__':
    main()
