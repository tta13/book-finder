from wrapper import *
import os, json

#from .wrapper import *

CRAWLED_DATA_PATH = '../data/crawled/'

def recall(c, n): return c / n

def precision(c, e): return c / e

def f_measure(r, p): return 2*(r*p)/(r+p)

def compare_extractions(key, generic_extraction, baseline_extraction):
    if generic_extraction == '': return False
    if key == 'authors':
        for a in baseline_extraction:
            if a in generic_extraction: return True
    elif key == 'edition': return generic_extraction in baseline_extraction
    else: return baseline_extraction in generic_extraction

def compare_strategies():
    extractions_possible, extractions_made, extractions_correct = 0, 0, 0
    recall, precision, f_measure
    for domain in os.listdir(WRAPPED_DATA_PATH):
        dir = os.path.join(WRAPPED_DATA_PATH, domain)
        if not os.path.isdir(dir): continue
        books = os.listdir(dir)
        books = zip(books[::2], books[1::2])
        for generic_file, baseline_file in books:
            with open(os.path.join(dir, generic_file), 'r', encoding='utf-8') as file:
                generic = json.load(file)
            with open(os.path.join(dir, baseline_file), 'r', encoding='utf-8') as file:
                baseline = json.load(file)
            for key in baseline:
                generic_extraction = generic[key]
                baseline_extraction = baseline[key]
                if baseline_extraction != '' and baseline_extraction != []:
                    extractions_possible += 1
                    if compare_extractions(key, generic_extraction, baseline_extraction):
                        extractions_correct += 1
                if generic_extraction != '' and generic_extraction != []:
                    extractions_made += 1
    file_path = os.path.join(WRAPPED_DATA_PATH, 'results.json')
    print(f"Saving results to: {file_path}")
    try:
        with open(file_path, 'w', encoding='utf-8') as outfile:
            r = recall(extractions_correct, extractions_possible)
            p = precision(extractions_correct, extractions_made)
            json.dump({
                'n': extractions_possible,
                'e': extractions_made,
                'c': extractions_correct,
                'recall': r,
                "precision": p,
                "f-measure": f_measure(r, p)

            }, outfile, ensure_ascii=False, indent=1)
    except Exception as e:
        print(f"Failed to save page info\n{e}")



def wrap_data():
    for wrapper in WrapperFactory().get_wrappers(CRAWLED_DATA_PATH):
        wrapper.wrap()

if __name__ == '__main__':
    #b = LivrariaFlorenceWrapper('../data/positive-bfs/').wrap()
    #b = LivrariaFlorenceWrapper('../data/positive-heu/').wrap()
    compare_strategies()
