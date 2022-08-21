import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


from bs4 import BeautifulSoup

from sklearn import metrics
import joblib
import numpy as np
import os
import shutil

class HTML_classifier():
    def __init__(self) -> None:
        package_directory = os.path.dirname(os.path.abspath(__file__))
        self.saved_model_path = os.path.join(package_directory, "finalized_model.sav")
        if os.path.exists(self.saved_model_path):
            self.saved_clf = joblib.load(self.saved_model_path)
        pass

    def predict_score(self, HTML):

        souper = []
        for htmls in HTML:
            arquive = open(htmls, encoding="utf8")
            soup = BeautifulSoup(arquive, 'html.parser')
            souper.append(soup.get_text())

        #x = [self.preprocess_url(HTML)]
        y = self.saved_clf.predict(souper) # format: [[prob_0, prob_1]]
        return (y) # returns prob of being a book page url

    def predict_list_html_hr(self, html_path_list):
        responses = []
        for html_path in html_path_list:
            responses += self.predict_score(html_path)
        harvest_ratio = sum(responses) / len(responses)
        return harvest_ratio
    
    def predict_subdirectory_hr(self, subdirectory):
        html_path_list = [os.path.join(subdirectory, f) for f in os.listdir(subdirectory)]
        results = self.predict_score(html_path_list)
        harvest_ratio = sum(results)/len(results)
        self.prepare_html_for_wrapper(subdirectory, html_path_list, results)
        return harvest_ratio
    
    def prepare_html_for_wrapper(self, subdirectory, html_path_list, results):
        dominio = subdirectory.split('-')[0]
        strategy = subdirectory.split('-')[1]
        destin_dir = os.path.join('..', '..', 'data', f'positive-{strategy}', dominio)
        html_file_list = os.listdir(subdirectory)
        if not os.path.exists(destin_dir):
            os.makedirs(destin_dir)
        for i in range(len(results)):
            destin_file = os.path.join(destin_dir, html_file_list[i])
            if results[i] == 1:
                shutil.copy(html_path_list[i], destin_file)
