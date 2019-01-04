# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 14:14:16 2018

@author: Sivaraman Lakshmipathy, Lakshmi Divya Jillellamudi Kamala
"""

#General imports
import os
import nltk
import pandas as pd
from nltk.corpus import stopwords

#Feature engineering imports
from sklearn.feature_extraction.text import TfidfVectorizer
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler
from imblearn.over_sampling import SMOTE

from nltk.stem import PorterStemmer
ps = PorterStemmer()

w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
lemmatizer = nltk.stem.WordNetLemmatizer()

def read_from_file(fileName):
    data = pd.read_csv(fileName, low_memory=False)
    return data

def lemmatize_text(text):
    lemma_str = ""
    for w in w_tokenizer.tokenize(text):
        lemma_str += lemmatizer.lemmatize(w) + " "
    return lemma_str

def stem_text(text):
    stem_str = ""
    for w in w_tokenizer.tokenize(text):
        stem_str += ps.stem(w) + " "
    return stem_str

def load_lexicon():
    ENGLISH_OPINION_LEXICON_LOCATION = os.path.join('opinion-lexicon-English')
    POS_WORDS_FILE = os.path.join(ENGLISH_OPINION_LEXICON_LOCATION, 'positive-words.txt')
    NEG_WORDS_FILE = os.path.join(ENGLISH_OPINION_LEXICON_LOCATION, 'negative-words.txt')

    pos_words = []
    neg_words = []

    for pos_word in open(POS_WORDS_FILE, 'r').readlines()[35:]:
        pos_words.append(pos_word.strip())

    for neg_word in open(NEG_WORDS_FILE, 'r').readlines()[35:]:
        neg_words.append(neg_word.strip())
    
    return pos_words, neg_words

def strip_column_names(data):
    data.rename(columns=lambda x:x.strip(), inplace=True)
    return data
    
def replace_comma(data):
    data['text'] = data['text'].str.lower()
    data['text'] = data['text'].str.replace('\[comma\]',',')
    return data
    
def load_stopwords():
    stopWords = set(stopwords.words('english'))
    return stopWords

def getFeaturesAndTarget(data):
    y = data["class"].copy()
    return getFeatures(data),y

def getFeatures(data):
    X = data["text"].copy()
    return X

def drop_long_sentences(data):
    drop_indx = []
    for index, row in data.iterrows():
        if len(row['text']) > 500:
            drop_indx.append(index)
    return drop_indx

def opinion_vector(text):
    global pos_words, neg_words
    opinion_val = 0
    for w in w_tokenizer.tokenize(text):
        if w in pos_words:
            opinion_val += 2
        elif w in neg_words:
            if opinion_val > 0:
                opinion_val -= 1
            else:
                opinion_val += 1
    return opinion_val

def calculate_tf_idf(X, stopWords):
    tf_vect = TfidfVectorizer(use_idf=True, stop_words = stopWords, ngram_range=(1,3))
    tf_vect.fit(X)
    X_tf = tf_vect.transform(X)
    return tf_vect, X_tf


def sample_data(X, y, sampleMethod):
    if sampleMethod == "Undersample":
        rus = RandomUnderSampler(return_indices=True)
        X_rus, y_rus, id_rus = rus.fit_sample(X, y)
        return X_rus, y_rus, id_rus
    elif sampleMethod == "Oversample":
        ros = RandomOverSampler()
        X_ros, y_ros = ros.fit_sample(X, y)
        return X_ros, y_ros
    elif sampleMethod == "SMOTE":
        smote = SMOTE(ratio='minority')
        X_sm, y_sm = smote.fit_sample(X, y)
        return X_sm, y_sm
    
pos_wt = 2
neg_wt = 1
def proximity_opinion_cal(text, aspect_term):
    global pos_wt, neg_wt
    #print("here")
    #print(text)
    #print(aspect_term)
    if not aspect_term in text:
        return 0
    indx_aspect_term = text.index(aspect_term)
    indx_fwd = indx_aspect_term + len(aspect_term)
    indx_bwd = indx_aspect_term
    str1 = text[:indx_bwd]
    str2 = text[indx_fwd:]
    #print(str1)
    #print(str2)
    str1_list = str1.split(" ")
    str2_list = str2.split(" ")
    #print(str1_list)
    #print(str2_list)
    i = len(str1_list) - 1
    j = 0
    op_list = []
    op_dist_wt = 0
    while i > 0 and j < len(str2_list):
        word1 = str1_list[i]
        dist_word1 = len(str1_list) - i
        if word1 in pos_words:
            op_list.append((word1, pos_wt, dist_word1))
            op_dist_wt += dist_word1
        elif word1 in neg_words:
            op_list.append((word1, neg_wt, dist_word1))
            op_dist_wt += dist_word1
        word2 = str2_list[j]
        dist_word2 = j + 1
        if word2 in pos_words:
            op_list.append((word2, pos_wt, dist_word2))
            op_dist_wt += dist_word2
        elif word2 in neg_words:
            op_list.append((word2, neg_wt, dist_word2))
            op_dist_wt += dist_word2
        i = i - 1
        j = j + 1
    while i > 0:
        word1 = str1_list[i]
        dist_word1 = len(str1_list) - i
        if word1 in pos_words:
            op_list.append((word1, pos_wt, dist_word1))
            op_dist_wt += dist_word1
        elif word1 in neg_words:
            op_list.append((word1, neg_wt, dist_word1))
            op_dist_wt += dist_word1
        i = i - 1
    while j < len(str2_list):
        word2 = str2_list[j]
        dist_word2 = j + 1
        if word2 in pos_words:
            op_list.append((word2, pos_wt, dist_word2))
            op_dist_wt += dist_word2
        elif word2 in neg_words:
            op_list.append((word2, neg_wt, dist_word2))
            op_dist_wt += dist_word2
        j = j + 1
    #print(len(op_list))
    #print(op_dist_wt)
    value = 0
    for entry in op_list:
        value += entry[2] / op_dist_wt * entry[1]
    #print(value)
    return value
    
def process_data(data):
    #strip extra spaces in column names
    data = strip_column_names(data)
    
    drop_indx = drop_long_sentences(data)
    data = data.drop(drop_indx)
    
    op_vector = []
    for i in range(data.text.shape[0]):
        op_vector.append(proximity_opinion_cal(data.text.iloc[i], data.aspect_term.iloc[i].lower().replace('"','')))
    print(len(op_vector))
    op_vector_series = pd.Series((entry for entry in op_vector))
    
    #replace [comma]
    data = replace_comma(data)
    
    #lemmatize text
    data['text'] = data.text.apply(lemmatize_text)
    
    return data, op_vector_series