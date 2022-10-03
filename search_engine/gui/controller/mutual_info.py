from search_engine.query import field_index
import numpy as np

def get_docids_intersection(terms):
    '''
    Returns a sorted array of docIDs representing the unique set of docs where all terms occur (intersection)
    '''
    terms_docs = []
    for index, term in enumerate(terms, start=0):
        if index > 0:
            terms_docs = set(terms_docs).intersection([doc_freq[0] for doc_freq in field_index.search_term(term)])
        else:
            terms_docs += [doc_freq[0] for doc_freq in field_index.search_term(term)]
        if len(terms_docs) == 0: return [] # If intersection is null before loop ends
    terms_docs = list(terms_docs)
    terms_docs.sort()
    return terms_docs

def get_top_k_mutualinfo(query, field, k=3):
    '''
    Returns a sorted by mutual information score array of terms (strings) representing 
    the top-K terms with largest mutual information with the input query
    (considering only terms from the specified field)
    '''
    p_query = len(get_docids_intersection(query)) # Amount of docs where all terms in query occur together
    if p_query == 0:
        return []
    top_k = []
    for term in field_index.vocab: # Iterate over inv. index vocab
        if term.split('.')[1] == field and term not in query: # Filter only terms from desired field and different from query words
            p_term = len([doc_freq[0] for doc_freq in field_index.search_term(term)]) # Amount of docs where term exists
            if p_term == 0:
                continue
            p_query_term = len(get_docids_intersection(query+[term])) # Amount of docs where the current term and all terms in query occur together
            if p_query_term == 0:
                continue
            mutualinfo_score = np.log2(p_query_term / (p_query * p_term))
            top_k.append((term, mutualinfo_score))
            if len(top_k) > k:
                top_k.sort(key= lambda x: -x[1]) # Descending sorting
                top_k.pop()
    return [term_score[0].split('.')[0] for term_score in top_k]
