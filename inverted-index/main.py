import os
import json
from inverted_index import create_doc_ids, build_inv_index, build_inv_index_fields

def save_json(path, name, content):
    if not os.path.exists(path):
        os.makedirs(path)
    file_path = os.path.join(path, name)
    print(f"Saving json file to: {file_path}")
    try:
        with open(file_path, 'w', encoding='utf-8') as outfile:
            json.dump(content, outfile, ensure_ascii=False, indent=1)
    except Exception:
        print(f"Failed to save json")

def load_doc_ids(path) -> dict:
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception:
        raise Exception

def save_doc_ids(doc_ids: dict):
    file_dir = os.path.join('..', 'data', 'inverted-index')
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    file_path = os.path.join(file_dir, 'docIDs.json')
    print(f"Saving doc IDs info to: {file_path}")
    try:
        with open(file_path, 'w', encoding='utf-8') as outfile:
            json.dump(doc_ids, outfile, ensure_ascii=False, indent=1)
    except Exception:
        print(f"Failed to save doc IDs")

def main():
    try:
        doc_ids = load_doc_ids(os.path.join('..', 'data', 'inverted-index', 'docIDs.json'))
    except Exception:
        doc_ids = create_doc_ids()
        save_doc_ids(doc_ids)
    
    path = os.path.join('..', 'data', 'inverted-index')
    save_json(path, 'fieldIndex.json', build_inv_index_fields(doc_ids))
    save_json(path, 'index.json', build_inv_index(doc_ids))

if __name__ == '__main__':
    main()