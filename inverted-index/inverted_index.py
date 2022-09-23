from io import BufferedReader, BufferedWriter
import os
import re
import json
import struct
from string import punctuation
from typing import Any, Tuple
from bs4 import BeautifulSoup

# Consts

SPACES = r'( )+'
PUNCTUATION = punctuation.replace('_', '').replace('$', '') + '“”’‘–−―…'

#region Pre-Processing

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

def pre_process_docs(doc_ids: dict, limit: int=None):
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

def pre_process_fields(doc_ids: dict, limit: int=None):
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

#endregion

#region Indexing 
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

def merge_index(term_docs: list[Tuple[str, int]]):
    result = {}
    last_term, last_doc = '', 0
    for term, doc in term_docs:
        if term not in result:
            result[term] = [(doc, 1)]
        elif term == last_term and doc == last_doc:
            doc, frequency = result[term].pop()
            frequency += 1
            result[term].append((doc, frequency))
        else: # term == last_term and doc != last_doc:
            result[term].append((doc, 1))
        last_term = term
        last_doc = doc
    return result    

def build_inv_index(doc_ids: dict):
    print('Building document inverted index...')
    term_document = []
    for doc_id, tokens in pre_process_docs(doc_ids):
        print(f'Processing doc: {doc_id}')
        for token in tokens:
            term_document.append((token, doc_id))
    term_document = sorted(term_document, key=lambda x: (x[0], x[1]))
    return merge_index(term_document)

def build_inv_index_fields(doc_ids: dict):
    print('Building field inverted index...')
    term_document = []
    for doc_id, tokens in pre_process_fields(doc_ids):
        print(f'Processing doc: {doc_id}')
        for token in tokens:
            term_document.append((token, doc_id))
    term_document = sorted(term_document, key=lambda x: (x[0], x[1]))
    return merge_index(term_document)
#endregion

#region Search
def binary_search(arr: list[Any], x: Any) -> int:
    low = 0
    high = len(arr) - 1
    mid = 0

    while low <= high:
 
        mid = (high + low) // 2
 
        # If x is greater, ignore left half
        if arr[mid] < x:
            low = mid + 1
 
        # If x is smaller, ignore right half
        elif arr[mid] > x:
            high = mid - 1
 
        # means x is present at mid
        else:
            return mid
 
    # If we reach here, then the element was not present
    return -1
#endregion

#region Compressing
def by4(f: BufferedReader):
    data = f.read()
    for i in range(0, len(data), 4):
        yield data[i:i+4]

def transform_binary_postings(postings: list):
    int_postings = [struct.unpack('i', value)[0] for value in postings]
    return [(x, y) for x, y in zip(int_postings[::2], int_postings[1::2])]

def transform_compressed_bytes_postings(postings: list):
    int_postings = [int(bytes_to_bitstring(b), 2) for b in postings]
    result = []
    acc_x = 0
    for x, y in zip(int_postings[::2], int_postings[1::2]):
        result.append((acc_x + x, y))
        acc_x += x
    return result

def encode_number(number: int):
    binary = decimal_to_binary(number)
    count = 0
    encoded_number = ''
    parts = 0
    for idx in range(len(binary), 0, -1):
        if count != 6:
            encoded_number = binary[idx-1] + encoded_number
            count += 1
        else:
            if parts == 0:
                encoded_number = '1' + binary[idx-1] + encoded_number
                parts += 1
            else:
                encoded_number = '0' + binary[idx-1] + encoded_number
                parts += 1
            count = 0
    if len(encoded_number) % 8 != 0:
        zeros_needed = 8 - (len(encoded_number) % 8)
        for idx in range(0, zeros_needed):
            if idx == zeros_needed - 1:
                if parts == 0:
                    encoded_number = '1' + encoded_number
                else:
                    encoded_number = '0' + encoded_number
            else:
                encoded_number = '0' + encoded_number
    
    return encoded_number

def decimal_to_binary(n: int):
    return f'{n:b}'

def str_by_8(s: str):
    for i in range(0, len(s), 8):
        yield s[i:i+8]

def by1(f: BufferedReader):
    data = f.read()
    for i in range(0, len(data), 1):
        yield data[i:i+1]

def bitstring_to_bytes(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')

def bytes_to_bitstring(b):
    return f'{int(b.hex(), base=16):08b}'
#endregion
    
class InvertedIndex:
    def __init__(self, inv_index: dict[str, list[Tuple[int, int]]]=None, compressed=True) -> None:
        self.inv_index = inv_index
        self.vocab = list(inv_index.keys()) if inv_index else None
        self.postings = list(inv_index.values()) if inv_index else None
        self.compressed = compressed

    def save_uncompressed(self, path, name):
        if not os.path.exists(path):
            os.makedirs(path)
        vocab_path = os.path.join(path, f'{name}-vocab.txt')
        postings_path = os.path.join(path, f'{name}-postings.txt')
        vocab_file = open(vocab_path, 'w', encoding="utf-8")
        postings_file = open(postings_path, 'wb')
        for term, postings in self.inv_index.items():
            vocab_file.write(f'{term}\n')
            for doc, freq in postings:
                postings_file.write(struct.pack('i', doc))
                postings_file.write(struct.pack('i', freq))
            postings_file.write(struct.pack('i', -1))
        vocab_file.close()
        postings_file.close()
        return self

    def write_encoded_number_to_file(self, file: BufferedWriter, n: int):
        new_n = encode_number(n)
        for byte in str_by_8(new_n):
            file.write(bitstring_to_bytes(byte))

    def save_compressed(self, path, name):
        if not os.path.exists(path):
            os.makedirs(path)
        vocab_path = os.path.join(path, f'{name}-vocab.txt')
        postings_path = os.path.join(path, f'{name}-postings-packed.txt')
        vocab_file = open(vocab_path, 'w', encoding="utf-8")
        postings_file = open(postings_path, 'wb')
        for term, postings in self.inv_index.items():
            vocab_file.write(f'{term}\n')
            last_doc = 0
            for doc, freq in postings:
                self.write_encoded_number_to_file(postings_file, doc - last_doc)
                self.write_encoded_number_to_file(postings_file, freq)
                last_doc = doc
            postings_file.write(bitstring_to_bytes('0'))
        vocab_file.close()
        postings_file.close()
        return self
    
    def save_to_file(self, path, name):
        if self.compressed: return self.save_compressed(path, name)
        return self.save_to_file(path, name)

    def load_vocab(self, vocab_path):
        vocab_file = open(vocab_path, 'r', encoding="utf-8")
        self.vocab = [word for word in vocab_file.read().splitlines()]        
        vocab_file.close()

    def load_uncompressed(self, vocab_path, postings_path):
        self.load_vocab(vocab_path)
        postings_file = open(postings_path, 'rb')
        i = 0
        self.postings = [[]]
        for rec in by4(postings_file):
            value, = struct.unpack('i', rec)
            if value == -1:
                i += 1
                self.postings.append([])
            else:
                self.postings[i].append(rec)
        self.postings = self.postings[:-1]
        postings_file.close()
        return self

    def load_compressed(self, vocab_path, postings_path):
        self.load_vocab(vocab_path)
        postings_file = open(postings_path, 'rb')
        i = 0        
        number = ''
        self.postings = [[]]
        for rec in by1(postings_file):
            s = bytes_to_bitstring(rec)
            if int(s, 2) == 0:
                i += 1
                self.postings.append([])
                continue
            elif s[0] == '1':
                number += s[1:]
                self.postings[i].append(bitstring_to_bytes(number))
                number = ''
            else: # s[0] == '0':
                number += s[1:]
        self.postings = self.postings[:-1]
        postings_file.close()
        return self

    def load_from_file(self, vocab_path, postings_path):
        if self.compressed: return self.load_compressed(vocab_path, postings_path)
        return self.load_uncompressed(vocab_path, postings_path)

    def search_term(self, term: str) -> list[Tuple[int, int]]:
        if not self.vocab: return []
        index = binary_search(self.vocab, term)
        if index < 0 or index >= len(self.vocab): return []
        
        if not self.compressed:
            return transform_binary_postings(self.postings[index])
        return transform_compressed_bytes_postings(self.postings[index])