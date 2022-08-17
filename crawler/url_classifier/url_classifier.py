from urllib.parse import urlparse
import pandas as pd
import re
import urllib.parse
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
import joblib
import numpy as np
import os

class url_classifier():
    def __init__(self) -> None:
        package_directory = os.path.dirname(os.path.abspath(__file__))
        self.saved_model_path = os.path.join(package_directory, "saved_model.joblib")
        if os.path.exists(self.saved_model_path):
            self.saved_clf = joblib.load(self.saved_model_path)
        pass

    def train_classifier(self, save=False):
        self.load_data()

        parameters = {
            'vect__ngram_range': [(1, 1), (1, 2)],
            'tfidf__use_idf': (True, False),
            'clf__alpha': (1e-1, 0.05, 1e-2),
        }

        self.url_clf = Pipeline([
            ('vect', CountVectorizer()),
            ('tfidf', TfidfTransformer()),
            #('clf', MultinomialNB()),
            #('clf', MLPClassifier(random_state=13, solver='adam', batch_size=1, hidden_layer_sizes=(4,), n_iter_no_change=8, tol=0.001)),
            ('clf', SGDClassifier(random_state=2, early_stopping=True, loss='modified_huber')),
        ])
        gs_clf = GridSearchCV(self.url_clf, parameters, n_jobs=2)
        self.url_clf = gs_clf.fit(self.x_train, self.y_train)

        print(gs_clf.best_score_)
        for param_name in sorted(parameters.keys()):
            print("%s: %r" % (param_name, gs_clf.best_params_[param_name]))
        if save:
            self.save_classifier()        

    def test_classifier(self):
        predicted = self.url_clf.predict(self.x_test)
        print("TEST ACCURACY: ", np.mean(predicted == self.y_test))
        print(metrics.classification_report(self.y_test, predicted))
        print(metrics.confusion_matrix(self.y_test, predicted))

        predicted = self.url_clf.predict(self.x_train)
        print("TRAIN ACCURACY: ", np.mean(predicted == self.y_train))
        print(metrics.classification_report(self.y_train, predicted))
        print(metrics.confusion_matrix(self.y_train, predicted))

    def save_classifier(self):
        joblib.dump(self.url_clf.best_estimator_, self.saved_model_path, compress = 1)
    
    def predict_score(self, url):
        x = [self.preprocess_url(url)]
        y = self.saved_clf.predict_proba(x) # format: [[prob_0, prob_1]]
        return (y[0][1]) # returns prob of being a book page url
    
    def load_data(self):
        data = pd.read_csv('labeled_urls.csv')
        data.drop(columns=['domínio'], inplace=True)
        data['url'] = data['url'].apply(self.preprocess_url)
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            data['url'], data['label'], shuffle=True, random_state=23, test_size=0.3
        )
    
    def remove_url_scheme_netloc(self, url):
        # keeps only url path, params and query strings
        parsed_url = urlparse(url)
        try:
            return f"{parsed_url.path}/{parsed_url.params}/{parsed_url.query}/{parsed_url.fragment}"
        except Exception:
            return url
    
    def unquote_url(self, url):
        # decode url characters and split query strings
        return urllib.parse.unquote_plus(url)
    
    def split_terms(self, url):
        # split url by replacing some special characters and removing numbers
        res = re.sub('[0-9]+', '', url)
        return re.sub('(\.|;|,|\*|\n|\/|-|_|!|\?|$|%|&|#|@|=){1,}', ' ', res)
    
    def preprocess_url(self, url):
        res = self.remove_url_scheme_netloc(url)
        res = self.unquote_url(res)
        res = self.split_terms(res)
        return res.lower()
