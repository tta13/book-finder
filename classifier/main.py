import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.pipeline import Pipeline
from bs4 import BeautifulSoup
import pathlib
import os
import numpy as np

import time


if __name__ == '__main__':
    df = pd.read_csv('rotulagem de dados.csv')

    print(pathlib.Path().resolve())

    lines2 = []

    # assign directory
    directory = '..\data\crawled_classifier'
 
    # iterate over files in
    # that directory
    counter = 0
    vectorizer = CountVectorizer()
    souper = []

    listofurls = []
    listoflabels = []


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
                #labellist = row['label'].tolist()
                #if(len(labellist) > 1):
                #    print(df.index[df['url'] == urllink].tolist())
                #    print(urllink)
                #print('labellist ' + str(labellist))
                label = row['label'].item()

                listofurls.append(urllink)
                listoflabels.append(label)

                acc +=1

        lines2 = []

    from sklearn.model_selection import train_test_split
    souper_train, souper_test, labels_train, labels_test = train_test_split(
    souper, listoflabels, test_size=0.3, random_state=42)
    
    #TREAT DATA
    X = vectorizer.fit_transform(souper_train)

    tfidf_transformer = TfidfTransformer()
    X_tf_train = tfidf_transformer.fit_transform(X)

    X_new_counts_test = vectorizer.transform(souper_test)
    X_new_tfidf_test = tfidf_transformer.transform(X_new_counts_test)

    ## FIRST TEST WITH CLASSIFIER
    from sklearn.naive_bayes import MultinomialNB
    start = time.time()
    text_clf = MultinomialNB().fit(X_tf_train, labels_train)
    stop = time.time()

    predicted = text_clf.predict(X_new_tfidf_test)

    print(len(souper_test))
    print(len(souper_train))

    from sklearn.metrics import precision_recall_fscore_support
    from sklearn.metrics import accuracy_score

    print("MultinomialNB   ")
    print("test :")
    precision, recall, f1, _ = precision_recall_fscore_support(labels_test, predicted, labels=[1, 0])
    acuracia = accuracy_score(labels_test, predicted)
    print("Accuracy:", acuracia)
    print("Precision:", precision)
    print("recall:", recall)
    print("f1:", f1)
    print(f"Training time: {stop - start}s")
    print('\n')

    print('==================')

    predicted = text_clf.predict(X_tf_train)
    print("train :")
    precision, recall, f1, _ = precision_recall_fscore_support(labels_train, predicted, labels=[1, 0])
    acuracia = accuracy_score(labels_train, predicted)
    print("Accuracy:", acuracia)
    print("Precision:", precision)
    print("recall:", recall)
    print("f1:", f1)
    print(f"Training time: {stop - start}s")
    print('\n')

    ###SVMCLASSIFIER/Gradient Bossting Classifier -> SVM
    from sklearn.linear_model import SGDClassifier
    start = time.time()
    text_clf2 = SGDClassifier(random_state=42).fit(X_tf_train, labels_train)
    stop = time.time()

    predicted = text_clf2.predict(X_new_tfidf_test)

    print("SGDClassifier   ")

    precision, recall, f1, _ = precision_recall_fscore_support(labels_test, predicted, labels=[1, 0])
    acuracia = accuracy_score(labels_test, predicted)
    print("Accuracy:", acuracia)
    print("Precision:", precision)
    print("recall:", recall)
    print("f1:", f1)
    print(f"Training time: {stop - start}s")
    
    print('\n')

    print('==================')

    predicted = text_clf2.predict(X_tf_train)
    print("train :")
    precision, recall, f1, _ = precision_recall_fscore_support(labels_train, predicted, labels=[1, 0])
    acuracia = accuracy_score(labels_train, predicted)
    print("Accuracy:", acuracia)
    print("Precision:", precision)
    print("recall:", recall)
    print("f1:", f1)
    print(f"Training time: {stop - start}s")
    print('\n')

    ###LogisticRegression

    from sklearn.linear_model import LogisticRegression
    start = time.time()
    
    text_clf3 = LogisticRegression(random_state=42).fit(X_tf_train, labels_train)
    stop = time.time()

    predicted = text_clf3.predict(X_new_tfidf_test)

    print("LogisticRegression   ")

    precision, recall, f1, _ = precision_recall_fscore_support(labels_test, predicted, labels=[1, 0])
    acuracia = accuracy_score(labels_test, predicted)
    print("Accuracy:", acuracia)
    print("Precision:", precision)
    print("recall:", recall)
    print("f1:", f1)
    print(f"Training time: {stop - start}s")
    
    print('\n')

    print('==================')

    predicted = text_clf3.predict(X_tf_train)
    print("train :")
    precision, recall, f1, _ = precision_recall_fscore_support(labels_train, predicted, labels=[1, 0])
    acuracia = accuracy_score(labels_train, predicted)
    print("Accuracy:", acuracia)
    print("Precision:", precision)
    print("recall:", recall)
    print("f1:", f1)
    print(f"Training time: {stop - start}s")
    print('\n')


    ###Decision Tree Classifier

    from sklearn.tree import DecisionTreeClassifier
    from sklearn import tree
    start = time.time()
    
    text_clf4 = DecisionTreeClassifier(random_state=42,criterion='entropy', max_depth = 4).fit(X_tf_train, labels_train)
    stop = time.time()
    
    predicted = text_clf4.predict(X_new_tfidf_test)

    print("DecisionTreeClassifier   ")

    precision, recall, f1, _ = precision_recall_fscore_support(labels_test, predicted, labels=[1, 0])
    acuracia = accuracy_score(labels_test, predicted)
    print("Accuracy:", acuracia)
    print("Precision:", precision)
    print("recall:", recall)
    print("f1:", f1)
    print(f"Training time: {stop - start}s")
    
    print('\n')

    print('==================')

    predicted = text_clf4.predict(X_tf_train)
    print("train :")
    precision, recall, f1, _ = precision_recall_fscore_support(labels_train, predicted, labels=[1, 0])
    acuracia = accuracy_score(labels_train, predicted)
    print("Accuracy:", acuracia)
    print("Precision:", precision)
    print("recall:", recall)
    print("f1:", f1)
    print(f"Training time: {stop - start}s")
    print('\n')

    ###Gradient Bossting Classifier/ SVM

    from sklearn.svm import SVC
    start = time.time()
    
    text_clf5 = SVC(random_state=42).fit(X_tf_train, labels_train)
    stop = time.time()

    predicted = text_clf5.predict(X_new_tfidf_test)

    print("SVM   ")

    precision, recall, f1, _ = precision_recall_fscore_support(labels_test, predicted, labels=[1, 0])
    acuracia = accuracy_score(labels_test, predicted)
    print("Accuracy:", acuracia)
    print("Precision:", precision)
    print("recall:", recall)
    print("f1:", f1)
    print(f"Training time: {stop - start}s")
    
    print('\n')

    print('==================')

    predicted = text_clf5.predict(X_tf_train)
    print("train :")
    precision, recall, f1, _ = precision_recall_fscore_support(labels_train, predicted, labels=[1, 0])
    acuracia = accuracy_score(labels_train, predicted)
    print("Accuracy:", acuracia)
    print("Precision:", precision)
    print("recall:", recall)
    print("f1:", f1)
    print(f"Training time: {stop - start}s")
    print('\n')

    ###Decision Tree Classifier
    from sklearn.neural_network import MLPClassifier
    start = time.time()
    
    text_clf6 = MLPClassifier(random_state=42, max_iter=300).fit(X_tf_train, labels_train)
    stop = time.time()
    
    predicted = text_clf6.predict(X_new_tfidf_test)

    print("MLP   ")

    precision, recall, f1, _ = precision_recall_fscore_support(labels_test, predicted, labels=[1, 0])
    acuracia = accuracy_score(labels_test, predicted)
    print("Accuracy:", acuracia)
    print("Precision:", precision)
    print("recall:", recall)
    print("f1:", f1)
    print(f"Training time: {stop - start}s")
    
    print('\n')

    print('==================')

    predicted = text_clf6.predict(X_tf_train)
    print("train :")
    precision, recall, f1, _ = precision_recall_fscore_support(labels_train, predicted, labels=[1, 0])
    acuracia = accuracy_score(labels_train, predicted)
    print("Accuracy:", acuracia)
    print("Precision:", precision)
    print("recall:", recall)
    print("f1:", f1)
    print(f"Training time: {stop - start}s")
    print('\n')

    ### DECISION TREE GRID SEARCH
    from sklearn.model_selection import GridSearchCV

    parameters = {'criterion':['gini','entropy'],'max_depth':[4,5,6,7,8,9,10,11,12,15,20,30,40,50,70,90,120,150], "min_samples_split": [2,5,7,10],
    "min_samples_leaf": [1,2,5]}

    gs_clf = GridSearchCV(DecisionTreeClassifier(random_state=42), parameters, cv=5, n_jobs=-1)
        
    start = time.time()
    
    gs_clf = gs_clf.fit(X_tf_train, labels_train)

    stop = time.time()

    print('best params: ')
    for param_name in sorted(parameters.keys()):
        print("%s: %r \n" % (param_name, gs_clf.best_params_[param_name]))

    from sklearn import metrics

    print('test ')
    predicted = gs_clf.best_estimator_.predict(X_new_tfidf_test)
    precision, recall, f1, _ = precision_recall_fscore_support(labels_test, predicted, labels=[1, 0])
    acuracia = accuracy_score(labels_test, predicted)
    print("Accuracy:", acuracia)
    print("Precision:", precision)
    print("recall:", recall)
    print("f1:", f1)
    print(metrics.confusion_matrix(labels_test, predicted))
    print(f"Training time: {stop - start}s")

    print('==================================')

    print('train ')
    predicted = gs_clf.best_estimator_.predict(X_tf_train)
    precision, recall, f1, _ = precision_recall_fscore_support(labels_train, predicted, labels=[1, 0])
    acuracia = accuracy_score(labels_train, predicted)
    print("Accuracy:", acuracia)
    print("Precision:", precision)
    print("recall:", recall)
    print("f1:", f1)
    print(metrics.confusion_matrix(labels_train, predicted))
    print(f"Training time: {stop - start}s")

    ## SVM GRID SEARCH

    # defining parameter range
    param_grid_SVC = {'C': [0.1, 1, 10, 100, 1000],
              'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
              'kernel': ['rbf']}
 
    grid_SVC = GridSearchCV(SVC(random_state=42), param_grid_SVC, refit = True, verbose = 3)
 
    start = time.time()

    # fitting the model for grid search
    grid_SVC.fit(X_tf_train, labels_train)

    stop = time.time()

    print('best params: ')
    for param_name in sorted(param_grid_SVC.keys()):
        print("%s: %r \n" % (param_name, grid_SVC.best_params_[param_name]))

    print('test ')
    predicted = grid_SVC.best_estimator_.predict(X_new_tfidf_test)
    precision, recall, f1, _ = precision_recall_fscore_support(labels_test, predicted, labels=[1, 0])
    acuracia = accuracy_score(labels_test, predicted)
    print("Accuracy:", acuracia)
    print("Precision:", precision)
    print("recall:", recall)
    print("f1:", f1)
    print(metrics.confusion_matrix(labels_test, predicted))
    print(f"Training time: {stop - start}s")

    print('==================================')

    print('train ')
    predicted = grid_SVC.best_estimator_.predict(X_tf_train)
    precision, recall, f1, _ = precision_recall_fscore_support(labels_train, predicted, labels=[1, 0])
    acuracia = accuracy_score(labels_train, predicted)
    print("Accuracy:", acuracia)
    print("Precision:", precision)
    print("recall:", recall)
    print("f1:", f1)
    print(metrics.confusion_matrix(labels_train, predicted))
    print(f"Training time: {stop - start}s")


    #Saving model
    import joblib

    svc_saved = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        #('clf', MultinomialNB()),
        #('clf', MLPClassifier(random_state=13, solver='adam', batch_size=1, hidden_layer_sizes=(4,), n_iter_no_change=8, tol=0.001)),
        ('clf', SVC(random_state=42)),
        ])

    svc_saved.fit(souper_train, labels_train)


    predicted = svc_saved.predict(souper_test)
    print("TEST ACCURACY: ", np.mean(predicted == labels_test))
    print(metrics.classification_report(labels_test, predicted))
    print(metrics.confusion_matrix(labels_test, predicted))

    predicted = svc_saved.predict(souper_train)
    print("TRAIN ACCURACY: ", np.mean(predicted == labels_train))
    print(metrics.classification_report(labels_train, predicted))
    print(metrics.confusion_matrix(labels_train, predicted))

    # save the model to disk
    model = svc_saved
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "HTMLClassifier","finalized_model.sav")
    joblib.dump(model, filename)

    ## load the model from disk
    #loaded_model = joblib.load(filename)
    #result = loaded_model.score(X_test, Y_test)
    #print(result)

