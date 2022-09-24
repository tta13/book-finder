import os
from inverted_index import (create_doc_ids, load_doc_ids, save_doc_ids, 
    save_field_inv_index, save_inv_index, load_field_inv_index, load_inv_index,
    DATA_PATH)

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