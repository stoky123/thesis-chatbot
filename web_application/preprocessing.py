import string
import pandas as pd
import re
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer


def remove_punctuation(text):
    punctuationfree = "".join([i for i in text if i not in string.punctuation])
    return punctuationfree


def tokenization(text):
    return text.split()


stopwords = nltk.corpus.stopwords.words('english')


def remove_stopwords(text):
    output = [i for i in text if i not in stopwords]
    return output


porter_stemmer = PorterStemmer()


def stemming(text):
    stem_text = [porter_stemmer.stem(word) for word in text]
    return stem_text


wordnet_lemmatizer = WordNetLemmatizer()


def lemmatizer(text):
    lemm_text = [wordnet_lemmatizer.lemmatize(word) for word in text]
    return lemm_text


def preprocess(sentence):
    sentence = remove_punctuation(sentence)
    sentence = sentence.lower()
    sentence = tokenization(sentence)
    sentence = remove_stopwords(sentence)
    sentence = stemming(sentence)
    sentence = lemmatizer(sentence)
    sentence = str(" ".join(sentence))

    return sentence
