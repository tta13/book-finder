import json
import os
from search_engine.inverted_index import *
import glob

query_response_mock = {
    13: 0.9,
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

def get_docmetadata(docname):
    base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', '..', 'data', 'wrapped')
    ends_with = '.html.json'
    filename = f"{docname}{ends_with}"
    path_list = [os.path.join(root, filename) for root, _, files in os.walk(base_path) if filename in files]
    docmetadata_path = path_list.pop()
    with open(docmetadata_path, encoding='utf-8') as file:
        return json.load(file)

def field_query(input):
    query = []
    for (field, value) in input.items():
        query += get_val_field_pairs(field, value)
    return search(query)

def text_query(input):
    query = tokenize_text(input)
    return search(query)

def search(query):
    if query:
    # call some function to obtain query response
    # docid_score = some_func(query)
        docid_score_result = query_response_mock # mocked response data
        results = []
        for docid, score in docid_score_result.items():
            docname = get_docid_name(docid)
            docurl = get_docname_url(docname)
            docmetadata = get_docmetadata(docname)
            docmetadata['url'] = docurl
            # print('\n',docname, '\n',docurl,'\n', docmetadata)
            results.append(docmetadata)
        return results
    return []