import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from bs4 import BeautifulSoup

import pathlib
import os

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
        #print(f)
        #print(filename)
        indexpath = os.path.join(f, 'index.txt')
        with open(indexpath) as reader:
            lines = reader.readlines()

        for line in lines:
            #print(line)
            word = line.split(' ')[-1]
            #print(word)
            line = word
            #print(line.strip())
            #print(line)
            lines2.append(line.strip())

        acc = 0
        for finalfile in os.listdir(f):
            htmls = os.path.join(f, finalfile)
            #print(str(finalfile))
            if(str(finalfile) == 'index.txt'):
                #print('skipped')
                continue
            if os.path.isfile(htmls):
                #print(htmls)
                arquive = open(htmls, encoding="utf8")
                soup = BeautifulSoup(arquive, 'html.parser')

                souper.append(soup.get_text()) 
                #print(souper)
                #X = vectorizer.fit_transform(souper)
                #print(vectorizer.get_feature_names_out())
                #print(X.shape)
                #print(X.toarray())


                #print('acc = ' + str(acc))
                urllink = lines2[acc]
                row = df.loc[df['url'] == urllink]
                labellist = row['label'].tolist()
                if(len(labellist) > 1):
                    print(df.index[df['url'] == urllink].tolist())
                    print(urllink)
                #print('labellist ' + str(labellist))
                label = row['label'].item()

                listofurls.append(urllink)
                listoflabels.append(label)

                acc +=1
                counter +=1

        lines2 = []

    from sklearn.model_selection import train_test_split
    souper_train, souper_test, labels_train, labels_test = train_test_split(
    souper, listoflabels, test_size=0.3, random_state=42)
    
    #TREAT DATA
    X = vectorizer.fit_transform(souper_train)

    tfidf_transformer = TfidfTransformer()
    #X_tf_train = tfidf_transformer.fit_transform(X)

    X_new_counts_test = vectorizer.transform(souper_test)
    #X_new_tfidf_test = tfidf_transformer.transform(X_new_counts_test)

    # tf_transformer = TfidfTransformer(use_idf=False).fit(X)
    # X_tf = tf_transformer.transform(X)

    # print('foi')

    ## FIRST TEST WITH CLASSIFIER
    from sklearn.naive_bayes import MultinomialNB
    #print(listoflabels)
    start = time.time()
    text_clf = MultinomialNB().fit(X, labels_train)
    stop = time.time()

    predicted = text_clf.predict(X_new_counts_test)

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

    predicted = text_clf.predict(X)
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
    text_clf2 = SGDClassifier(random_state=42).fit(X, labels_train)
    stop = time.time()

    predicted = text_clf2.predict(X_new_counts_test)

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

    predicted = text_clf2.predict(X)
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
    
    text_clf3 = LogisticRegression(random_state=42).fit(X, labels_train)
    stop = time.time()

    predicted = text_clf3.predict(X_new_counts_test)

    # text_clf3.fit(souper, listoflabels)

    #predicted = text_clf3.predict(placeholder)

    # for doc, category in zip(docs_new, predicted):
    #     print(doc)
    #     print(category)

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

    predicted = text_clf3.predict(X)
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
    
    #text_clf4 = DecisionTreeClassifier(criterion='entropy', max_depth = 5).fit(X, labels_train)
    text_clf4 = DecisionTreeClassifier(random_state=42,criterion='entropy', max_depth = 4).fit(X, labels_train)
    stop = time.time()
    
    predicted = text_clf4.predict(X_new_counts_test)

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

    predicted = text_clf4.predict(X)
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
    
    text_clf5 = SVC(random_state=42).fit(X, labels_train)
    stop = time.time()

    predicted = text_clf5.predict(X_new_counts_test)

    # text_clf5 = Pipeline([
    #     ('vect', CountVectorizer()),
    #     ('tfidf', TfidfTransformer()),
    #     ('clf', SVC()) #step2 - classifier,
    # ])

    # text_clf5.fit(souper, listoflabels)

    #predicted = text_clf5.predict(placeholder)

    # for doc, category in zip(docs_new, predicted):
    #     print(doc)
    #     print(category)

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

    predicted = text_clf5.predict(X)
    print("train :")
    precision, recall, f1, _ = precision_recall_fscore_support(labels_train, predicted, labels=[1, 0])
    acuracia = accuracy_score(labels_train, predicted)
    print("Accuracy:", acuracia)
    print("Precision:", precision)
    print("recall:", recall)
    print("f1:", f1)
    print(f"Training time: {stop - start}s")
    print('\n')

    ### GRID SEARCH
    from sklearn.model_selection import GridSearchCV

    #Cs = [0.0001,0.001, 0.01, 0.1, 1, 10]
    #parameters = {
    #    'alpha': Cs,
    #}

    parameters = {'criterion':['gini','entropy'],'max_depth':[4,5,6,7,8,9,10,11,12,15,20,30,40,50,70,90,120,150], "min_samples_split": [2,5,7,10],
    "min_samples_leaf": [1,2,5]}

    gs_clf = GridSearchCV(DecisionTreeClassifier(random_state=42), parameters, cv=5, n_jobs=-1)
        
    start = time.time()
    
    gs_clf = gs_clf.fit(X, labels_train)

    stop = time.time()

    print(gs_clf.best_score_)

    print('best params: ')
    for param_name in sorted(parameters.keys()):
        print("%s: %r \n" % (param_name, gs_clf.best_params_[param_name]))

    #print('results:  ')
    #print(gs_clf.cv_results_)

    from sklearn import metrics

    print('test ')
    predicted = gs_clf.best_estimator_.predict(X_new_counts_test)
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
    predicted = gs_clf.best_estimator_.predict(X)
    precision, recall, f1, _ = precision_recall_fscore_support(labels_train, predicted, labels=[1, 0])
    acuracia = accuracy_score(labels_train, predicted)
    print("Accuracy:", acuracia)
    print("Precision:", precision)
    print("recall:", recall)
    print("f1:", f1)
    print(metrics.confusion_matrix(labels_train, predicted))
    print(f"Training time: {stop - start}s")


    #df = pd.read_csv('rotulagem de dados.csv')
    #test = 0
    #for index, row in df.iterrows():
    #    df['html'] = CrawlerFactory().make_crawler(url=row['url'], pages_limit=1).run()

