# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 14:24:12 2018

@author: Sivaraman Lakshmipathy, Lakshmi Divya Jillellamudi Kamala
"""

import sys

#module imports
import absa_utils

#Persistence imports
import pickle
from scipy.sparse import hstack

def persistPrediction(ids, predictions, output_file):
    endline = "\n"
    file_obj = open(output_file, "w")
    
    i = 0
    for entry in ids:
        strToFile = entry + ";;" + str(predictions[i])
        strToFile += endline
        file_obj.write(strToFile)
        i = i+1
        
    file_obj.close()

def main():
    input_file = "data-1_train.csv"
    output_file = "absa_predictions.txt"
    model_fileName = "absa_train.sav"
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    data = absa_utils.read_from_file(input_file)
    
    absa_utils.pos_words, absa_utils.neg_words = absa_utils.load_lexicon()
    
    data = absa_utils.process_data(data)
    
    #fetch opinion vector
    test_op = data.text.apply(absa_utils.opinion_vector)
    X = absa_utils.getFeatures(data)
    tf_vect = pickle.load(open("tf_vect.sav", 'rb'))
    X_tf = tf_vect.transform(X)
    X_dtm = hstack((X_tf,test_op[:,None])).A
    
    trained_model = pickle.load(open(model_fileName, 'rb'))
    y_pred = trained_model.predict(X_dtm)
    
    persistPrediction(data["example_id"], y_pred, output_file)

if __name__ == '__main__':
    main()  

