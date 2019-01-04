# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 12:18:18 2018

@author: Sivaraman Lakshmipathy, Lakshmi Divya Jillellamudi Kamala

Aspect Based Sentiment Analysis source code
"""

#General imports
import sys

#module imports
import absa_utils
import absa_classifiers

#Feature engineering imports
from scipy.sparse import hstack

#Persistence imports
import pickle

import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")
        
def train_classifier_best(data, performance_measure):
    absa_utils.pos_words, absa_utils.neg_words = absa_utils.load_lexicon()
    data, op_vector = absa_utils.process_data(data)
    stopWords = absa_utils.load_stopwords()
    X, y = absa_utils.getFeaturesAndTarget(data)
    tf_vect, X_tf = absa_utils.calculate_tf_idf(X, stopWords)
    pickle.dump(tf_vect, open("tf_vect.sav", 'wb'))
    X_dtm = hstack((X_tf,op_vector[:,None])).A
    #sampling
    X_smpl, y_smpl = absa_utils.sample_data(X_dtm, y, "Oversample")
    svm_model = absa_classifiers.svm_classifier_train(X_smpl, y_smpl, performance_measure)
    return svm_model
    
def main():
    input_file = "data-1_train.csv"
    performance_measure = False
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == "--performance":
        performance_measure = True
    data = absa_utils.read_from_file(input_file)
    model = train_classifier_best(data, performance_measure)
    filename = 'absa_train.sav'
    pickle.dump(model, open(filename, 'wb'))

if __name__ == '__main__':
    main()  
