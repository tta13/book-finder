import os
import json
from inverted_index import create_doc_ids, build_inv_index, build_inv_index_fields, InvertedIndex

PATH = os.path.join('..', 'data', 'inverted-index')
INDEX_FILENAME = 'index'
FIELD_INDEX_FILENAME = 'fieldIndex'

def load_doc_ids(path) -> dict:
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception:
        raise Exception

def save_doc_ids(doc_ids: dict):
    if not os.path.exists(PATH):
        os.makedirs(PATH)
    file_path = os.path.join(PATH, 'docIDs.json')
    print(f"Saving doc IDs info to: {file_path}")
    try:
        with open(file_path, 'w', encoding='utf-8') as outfile:
            json.dump(doc_ids, outfile, ensure_ascii=False, indent=1)
    except Exception:
        print(f"Failed to save doc IDs")

def save_field_inv_index(doc_ids):    
    inv_index = build_inv_index_fields(doc_ids)
    index = InvertedIndex(inv_index).save_to_file(PATH, FIELD_INDEX_FILENAME)
    del inv_index
    del index

def load_field_inv_index():
    return InvertedIndex().load_from_file(os.path.join(PATH, f'{FIELD_INDEX_FILENAME}-vocab.txt'), os.path.join(PATH, f'{FIELD_INDEX_FILENAME}-postings.txt'))

def save_inv_index(doc_ids):
    inv_index = build_inv_index(doc_ids)
    index = InvertedIndex(inv_index).save_to_file(PATH, INDEX_FILENAME)
    del inv_index
    del index

def load_inv_index():
    return InvertedIndex().load_from_file(os.path.join(PATH, f'{INDEX_FILENAME}-vocab.txt'), os.path.join(PATH, f'{INDEX_FILENAME}-postings.txt'))

def main():
    try:
        doc_ids = load_doc_ids(os.path.join(PATH, 'docIDs.json'))
    except Exception:
        doc_ids = create_doc_ids()
        save_doc_ids(doc_ids)

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

    # Showing terms and postings on indexes
    print(len(field_index.vocab), len(field_index.postings))
    print(len(index.vocab), len(index.postings))
    
    # Making queries to field inverted index
    search_keys = ['ziraldo.author', 'orwell.description', 'orwell.author', 'marx.title', 'bichos.title', 'ágora.publisher']
    for key in search_keys:
        print(f'search: {key}\nresult: {field_index.search_term(key)}\n')
    
    # Making queries to inverted index
    search_keys = ['água', 'orwell', 'ágora', 'marx', 'vasco', 'fluminense', 'livro']
    for key in search_keys:
        print(f'search: {key}\nresult: {index.search_term(key)}\n')
    
if __name__ == '__main__':
    main()