# Index Program
# Author: Cristina Menghini 

from Index_lib import *

stopWord = stopwords.words('italian')
stemmerSnow = SnowballStemmer("italian")


list_post = engine_BoW('Documents') # Returns the list of the postings lists of each advertisement.

IndexDir = CreateIndexDir(os.getcwd()) # Creation of the /Index directory.

Voc_creation(list_post, IndexDir) # Returns vocabulary.txt.

Index(list_post, IndexDir) #Returns postings.txt.
