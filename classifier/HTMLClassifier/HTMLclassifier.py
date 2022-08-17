import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


from bs4 import BeautifulSoup

from sklearn import metrics
import joblib
import numpy as np
import os

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
        print(y)
        return (y) # returns prob of being a book page url