# Collect Program
# Author: Cristina Menghini 

from Collect_lib import *
from sys import argv
script , min_ki , max_ki , min_Im , max_Im , min_At , max_At= argv


#The first thing to do to create the search engine is building the collection on which the search will be done.

DocDir = CreateDIR(os.getcwd()) # Creation of /Documents directory

CreateAllDocs('Sites.txt' , DocDir, int(min_ki),int(max_ki),int(min_Im), int(max_Im), int(min_At),int(max_At) ) 

#Once the documents have been stored in /Documents directory, due to the high number of documents, I create subfolders, named documents-000001-000500 and so on, and each one contains the corrisponding files.

Subdirs(500, DocDir)
