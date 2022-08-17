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

    def get_labeled_htmls(self):
        df = pd.read_csv('rotulagem de dados.csv')
        # assign directory
        directory = '..\..\data\crawled_classifier'
        vectorizer = CountVectorizer()
        souper = []

        listofurls = []
        listoflabels = []

        lines2 = []
        # FIND AND DEAL WITH DATA
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)

            indexpath = os.path.join(f, 'index.txt')
            with open(indexpath) as reader:
                lines = reader.readlines()

            for line in lines:
                word = line.split(' ')[-1]
                line = word
                lines2.append(line.strip())
            
            acc = 0
            for finalfile in os.listdir(f):
                htmls = os.path.join(f, finalfile)
                if(str(finalfile) == 'index.txt'):
                    continue
                if os.path.isfile(htmls):
                    arquive = open(htmls, encoding="utf8")
                    soup = BeautifulSoup(arquive, 'html.parser')

                    souper.append(soup.get_text()) 
                    urllink = lines2[acc]
                    row = df.loc[df['url'] == urllink]
                    label = row['label'].item()

                    listofurls.append(urllink)
                    listoflabels.append(label)

                acc +=1

            lines2 = []

        return souper,listoflabels

    def predict_score(self, HTML):
        htmls,labels = self.get_labeled_htmls()
        
        souper_train, souper_test, labels_train, labels_test = train_test_split(
    htmls, labels, test_size=0.3, random_state=42)

        vectorizer = CountVectorizer()

        self.vectorized_train = vectorizer.fit_transform(souper_train)
        tfidf_transformer = TfidfTransformer()
        self.vectorized_tf_train = tfidf_transformer.fit_transform(self.vectorized_train)

        arquive = open(HTML, encoding="utf8")
        soup = BeautifulSoup(arquive, 'html.parser')

        vectorized_HTML = vectorizer.transform([soup.get_text()])
        transformedtfid_HTML = tfidf_transformer.transform(vectorized_HTML)

        y = self.saved_clf.predict(transformedtfid_HTML)# format: [[prob_0, prob_1]]

        print(y)
        return (y) # returns prob of being a book page url