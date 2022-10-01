import json
import os
from search_engine.inverted_index import *

query_response_mock = {
    13: 0.9,
    21: 0.54,
    5000: 0.1321,
    3200: 0.02
}

def get_val_field_pairs(field, value):
    return [f'{val}.{field}' for val in tokenize_text(value)]

docname_docid_map = {}
with open(os.path.join('..', '..', 'data', 'inverted-index', 'docIDs.json'), 'r', encoding='utf-8') as file:
    docname_docid_map = json.load(file)
def get_docid_name(docid):
    return list(docname_docid_map.keys())[list(docname_docid_map.values()).index(docid)]

docname_docurl_map = {}
with open(os.path.join('static', 'data', 'doc_name_to_url.json'), 'r', encoding='utf-8') as file:
    docname_docurl_map = json.load(file)
def get_docname_url(docname):
    return docname_docurl_map[docname]

def field_query(input):
    '''
    preprocess input to form a query as:
    query = [value.field]
    '''
    query = []
    for (field, value) in input.items():
        query += get_val_field_pairs(field, value)

    # call some function to obtain response
    # docid_score = some_func(query)
    docid_score_result = query_response_mock

    results = []
    for docid, score in docid_score_result.items():
        docname = get_docid_name(docid)
        docurl = get_docname_url(docname)
        print(docname, docurl)
        # get doc json
        # sum result object to results array

    return results

def text_query(input):
    pass