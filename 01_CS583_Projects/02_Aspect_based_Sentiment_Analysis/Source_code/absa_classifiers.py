# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 14:15:48 2018

@author: Sivaraman Lakshmipathy, Lakshmi Divya Jillellamudi Kamala
"""

#General imports
import numpy as np

#Feature engineering imports
from sklearn.model_selection import train_test_split

#Classifier imports
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import LinearSVC

#Validation imports
from sklearn import model_selection, metrics

def logisticRegression_classifier_train_validate(X, y, testSize):
    print("Logistic Regression")
    log_reg = LogisticRegression()
    preds = model_selection.cross_val_predict(log_reg, X, y, cv=10)
    accScore = metrics.accuracy_score(y,preds)
    labels = [-1, 0, 1]
    precision = metrics.precision_score(y,preds,average=None,labels=labels)
    recall = metrics.recall_score(y,preds,average=None,labels=labels)
    f1Score = metrics.f1_score(y,preds,average=None,labels=labels)
    print("\nOverall Acurracy - Logreg 2: ",accScore,"\n")
    for i in range(len(labels)):
        print("Precision of %s class: %f" %(labels[i],precision[i]))
        print("Recall of %s class: %f" %(labels[i],recall[i]))
        print("F1-Score of %s class: %f" %(labels[i],f1Score[i]),"\n")
        
def logisticRegression_classifier_train(X, y):
    log_reg = LogisticRegression()
    log_reg.fit(X, y)
    return log_reg

def adaBoost_classifier_train_validate(X, y, testSize, baseClassifier):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=testSize)
    # Create adaboost classifer object
    abc = AdaBoostClassifier(n_estimators=50,
                         learning_rate=1,
                        base_estimator=baseClassifier)
    # Train Adaboost Classifer
    model = abc.fit(X_train, y_train)

    #Predict the response for test dataset
    y_pred = model.predict(X_test)
    print(np.mean(y_pred == y_test))
    
def adaBoost_classifier_train(X, y, baseClassifier):
    abc = AdaBoostClassifier(n_estimators=50,
                         learning_rate=1,
                        base_estimator=baseClassifier)
    # Train Adaboost Classifer
    model = abc.fit(X, y)
    return model

def svm_classifier_train_validate(X, y, testSize):
    svc_clf = LinearSVC(multi_class='crammer_singer', random_state=0)
    preds = model_selection.cross_val_predict(svc_clf, X, y, cv=10)
    accScore = metrics.accuracy_score(y,preds)
    labels = [-1, 0, 1]
    precision = metrics.precision_score(y,preds,average=None,labels=labels)
    recall = metrics.recall_score(y,preds,average=None,labels=labels)
    f1Score = metrics.f1_score(y,preds,average=None,labels=labels)
    print("\nOverall Acurracy - SVM: ",accScore,"\n")
    for i in range(len(labels)):
        print("Precision of %s class: %f" %(labels[i],precision[i]))
        print("Recall of %s class: %f" %(labels[i],recall[i]))
        print("F1-Score of %s class: %f" %(labels[i],f1Score[i]),"\n")
        
def svm_classifier_train(X, y, performance_measure):
    svc_clf = LinearSVC(multi_class='crammer_singer', random_state=0)
    print("SVM")
    svc_clf.fit(X, y)
    if performance_measure == True:
        svm_classifier_train_validate(X, y, -1)
    return svc_clf

def multinomialNB_classifier_train_validate(X, y, testSize):
    print("MultinomialNB")
    nb = MultinomialNB()
    preds = model_selection.cross_val_predict(nb, X, y, cv=10)
    accScore = metrics.accuracy_score(y,preds)
    labels = [-1, 0, 1]
    precision = metrics.precision_score(y,preds,average=None,labels=labels)
    recall = metrics.recall_score(y,preds,average=None,labels=labels)
    f1Score = metrics.f1_score(y,preds,average=None,labels=labels)
    print("\nOverall Acurracy - Multi Naive Bayes: ",accScore,"\n")
    for i in range(len(labels)):
        print("Precision of %s class: %f" %(labels[i],precision[i]))
        print("Recall of %s class: %f" %(labels[i],recall[i]))
        print("F1-Score of %s class: %f" %(labels[i],f1Score[i]),"\n")
        
def multinomialNB_classifier_train(X, y):
    nb = MultinomialNB()
    nb.fit(X, y)
    return nb
