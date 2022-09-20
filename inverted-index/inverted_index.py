import os
import re
import json
from string import punctuation
from typing import Tuple
from bs4 import BeautifulSoup

SPACES = r'( )+'
PUNCTUATION = punctuation.replace('_', '')

def create_doc_ids():
    paths = ['../data/positive-bfs/', '../data/positive-heu/']
    doc_ids = {}
    curr_id = 0
    for path in paths:
        for domain in os.listdir(path):
            dir = os.path.join(path, domain)
            if not os.path.isdir(dir): continue
            for book in os.listdir(dir):
                if book.endswith('.html'):
                    book = book.replace('.html', '')
                    if book in doc_ids: continue
                    doc_ids[book] = curr_id
                    curr_id += 1
    return doc_ids

def to_lower(text: str) -> str:
    return text.lower()

def sub_spaces(text: str) -> str:
    spaces = re.compile(SPACES)
    text = spaces.sub(' ', text)
    return text.strip()

def remove_punctuation(text: str) -> str: 
    return text.translate(str.maketrans('', '', PUNCTUATION))

def tokenize_text(text: str) -> list[str]:
    if not text: return ['']
    text = to_lower(text)
    text = remove_punctuation(text)
    text = sub_spaces(text)
    return text.split()

def tokenize_fields(fields):
    # title
    texts = tokenize_text(fields['title'])
    title = [f'{t}.title' for t in texts if t]
    # author
    authors = fields['authors']
    if not authors:
        author = []
    else:
        texts = [tokenize_text(author) for author in authors]
        author = [f'{name}.author' for names in texts for name in names]
    # publisher
    texts = tokenize_text(fields['publisher'])
    pub = [f'{t}.publisher' for t in texts if t]
    # description
    texts = tokenize_text(fields['info'])
    desc = [f'{t}.description' for t in texts if t]
    return title + author + pub + desc 

def pre_process_docs(doc_ids: dict, limit=None):
    paths = ['../data/positive-bfs/', '../data/positive-heu/']
    processed_files = 0
    for path in paths:
        for domain in os.listdir(path):
            dir = os.path.join(path, domain)
            if not os.path.isdir(dir): continue
            for book in os.listdir(dir):
                if limit and processed_files >= limit: break
                if book.endswith('.html'):
                    file = os.path.join(dir, book)
                    html = open(file, 'r', encoding='utf-8')
                    text = BeautifulSoup(html, 'html.parser').get_text()
                    doc_id = doc_ids[book.replace('.html', '')]
                    tokens = tokenize_text(text)
                    processed_files += 1
                    yield doc_id, tokens

def pre_process_fields(doc_ids: dict, limit=None):
    path = '../data/wrapped/'
    processed_files = 0
    for domain in os.listdir(path):
        dir = os.path.join(path, domain)
        if not os.path.isdir(dir): continue
        for book in os.listdir(dir):
            if limit and processed_files >= limit: break
            if book.endswith('.generic.json'): continue

            if book.endswith('.json'):
                file = os.path.join(dir, book)
                json_file = open(file, 'r', encoding='utf-8')
                fields = json.load(json_file)
                doc_id = doc_ids[book.replace('.html.json', '')]
                tokens = tokenize_fields(fields)
                processed_files += 1
                yield doc_id, tokens

def merge_index(term_docs: list[Tuple[str, int]]):
    result = {}
    for term, doc in term_docs:
        if term not in result:
            result[term] = {doc: 1}
        else:
            if doc not in result[term]:
                result[term][doc] = 1
            else:
                result[term][doc] += 1
    return result    

def build_inv_index(doc_ids: dict):
    print('Building document inverted index...')
    term_document = []
    for doc_id, tokens in pre_process_docs(doc_ids):
        print(f'Processing doc: {doc_id}')
        for token in tokens:
            term_document.append((token, doc_id))
    term_document = sorted(term_document, key=lambda x: x[0])
    return merge_index(term_document)

def build_inv_index_fields(doc_ids: dict):
    print('Building field inverted index...')
    term_document = []
    for doc_id, tokens in pre_process_fields(doc_ids):
        print(f'Processing doc: {doc_id}')
        for token in tokens:
            term_document.append((token, doc_id))
    term_document = sorted(term_document, key=lambda x: x[0])
    return merge_index(term_document)
