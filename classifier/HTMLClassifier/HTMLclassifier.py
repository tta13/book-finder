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
import pathlib
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
        y = self.saved_clf.predict(souper)
        return (y)

    def predict_all_subdirs_hr(self, base_dir):
        subdirs_list = [os.path.join(base_dir, f) for f in os.listdir(base_dir)]
        for dir in subdirs_list:
            print(f'Starting to predict {dir} files...')
            print(f'[HARVEST RATIO] {dir} HR = ',self.predict_subdirectory_hr(dir),'\n')
    
    def predict_subdirectory_hr(self, subdirectory):
        html_path_list = [os.path.join(subdirectory, f) for f in os.listdir(subdirectory)]
        results = self.predict_score(html_path_list)
        harvest_ratio = sum(results)/len(results)
        self.prepare_html_for_wrapper(html_path_list, results)
        return harvest_ratio
    
    def prepare_html_for_wrapper(self, html_path_list, results):
        if html_path_list:
            path = pathlib.PurePath(html_path_list[0])
            dominio = path.parent.name.split('-')[0]
            strategy = path.parent.name.split('-')[1]
            destin_dir = os.path.join('..', '..', 'data', f'positive-{strategy}', dominio)
            if not os.path.exists(destin_dir):
                os.makedirs(destin_dir)
            print(f'Writing positive files to {destin_dir}...')
            for i in range(len(results)):
                if results[i] == 1:
                    destin_file = os.path.join(destin_dir, os.path.basename(html_path_list[i]))
                    shutil.copy(html_path_list[i], destin_file)
