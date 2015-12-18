# Index library
# Author: Cristina Menghini - StudentID: 1527821

import nltk
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from unicodedata import normalize
from nltk.stem import *
from nltk.stem.snowball import SnowballStemmer
import os
import pandas as pd
from nltk.probability import FreqDist

stopWord = stopwords.words('italian')
stemmerSnow = SnowballStemmer("italian")

def Tokenization(s):
# This function returns the list of all the words in the document.
#- string_name is the name of the string I want to toke
    punSet = set(string.punctuation)
    for char in punSet: #se s
        s = s.replace(char, ' ') 
    tokens = word_tokenize(s)
    return tokens

def Rem_stopwords(string_name, stopW):
#This function gives back the bag of words related to a document removing stopwords.
#- string_name is the name of file that is processing( string);
    morestopwords = [u'vendo',u'vendesi',u'mappa', u'nome', u'indirizzo', u'situato']
    for word in morestopwords:
        stopW.append(word)
    stopDict = {w : None for w in stopW}
    bag_words = [toke for toke in Tokenization(string_name) if toke not in stopDict ]
    return bag_words

def Normalization(stringname):
# This function returns the list of words cleaned from accent.
#- stringname filename is the string that contains the name of the doc and, eventually, its path.
    word_list = [normalize('NFKD', s).encode('ascii','ignore') for s in Rem_stopwords(stringname, stopWord)]
    return word_list

def Stemming(stringname, stemmer):
# This function return the list of words stemmed.
#- stringname is the name of the file to stemm( string).
    norm_text = Normalization(stringname)
    bag_of_words = [stemmer.stem(word) for word in norm_text] 
    for word in bag_of_words:
        if len(word) < 1 :
            bag_of_words.remove(word)
    return [w for w in bag_of_words if len(w) > 0]

def engine_BoW(big_dir):
# This function returns the list of the word stes of each advertise.
#- big_dir is the path of directory that contains all the docs and the subfolders(it's a string);
    list_postings = []
    list_sub_sort = sorted(os.listdir(big_dir))[:]
    for dirs in list_sub_sort:
        split_dir = dirs.split('-')
        endpoint_min = split_dir[1]
        for fname in sorted(os.listdir(big_dir+'/'+dirs)):
            with open(big_dir+'/'+dirs+'/'+fname, 'r+') as f:
                f1 =f.read().lower().decode('utf-8').replace("'",' ').split('\t')
                del f1[3]
                f = '\t'.join(f1)
                list_postings.append(Stemming(f, stemmerSnow))
    return list_postings     

def CreateIndexDir(path):
# This function creates the directory Index and returns the entire path of the new dir.
#- path is a string and corresponds to the path of the directory Index.
    try: 
        os.makedirs(path+'/Index')
    except OSError:
        if not os.path.isdir(path+'/Index'):
            raise
    return path+'/Index'


def Voc_creation(list_pos, directory): 
# This function return the file 'vocabulary.txt' organized as termID <tab> term
#- lis_pos is the return of engine_BoW
#- directory is the return of CreateIndexDir function
    word_set_1 = [list_pos[j][i] for j in range(len(list_pos)) for i in range(len(list_pos[j]))]
    word_set_list_sorted =sorted(list(set(word_set_1)))
    key = range(1, len(word_set_list_sorted)+1)
    vocabulary = pd.DataFrame({'key': key, 'term':word_set_list_sorted})
    vocabulary.to_csv(directory+'/vocabulary.txt', sep = '\t', header = False, index = False)  


def Index(list_word, directory):
# It returns the text file 'posting.txt'.
#- list_word: the return of engine_BoW function;
#- directory is the folder in which I store the file. It is the return of the function CreateIndexDir.
    list_tuples = [(list_word[j][i],j+1) for j in range(len(list_word)) for i in range(len(list_word[j]))] 
    list_tuples_set_sorted = sorted(list(set(list_tuples)))
    d = {}
    for k,v in list_tuples_set_sorted:
        d.setdefault(k,[]).append(v)
    index = sorted(d.items())
    key = range(1,len(index)+1)
    with open(directory+'/postings.txt', 'w') as f:
        for i in range(len(index)):
            f.write(str(key[i])+'\t'+ '\t'.join(map(lambda x: str(x), index[i][1]))+'\n')
