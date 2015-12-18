# Search Program
# Author: Cristina Menghini 

from Search_lib import *

stopWord = stopwords.words('italian')
stemmerSnow = SnowballStemmer("italian")

posting_in_mem = Memory_PostList('Index'+'/postings.txt') # Creates in memory the postings lists

vocab_in_mem = MapOfTerms('Index'+'/vocabulary.txt', posting_in_mem) # Vocabulary in memory

query = raw_input('Search:').decode('utf-8') # Query entered by the user
proc_query = Stemming(query, stemmerSnow) # Processed query

ansquery = AnsToQuery(proc_query, vocab_in_mem) # Verify the presence of the query in the vocabulary

if ansquery != None:
    AnsToUser('Documents' , ansquery)  # gives back the ads that match the query
else:
    print 'Your query does not match any advertisement.'
