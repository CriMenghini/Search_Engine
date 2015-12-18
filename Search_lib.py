# Search library
# Author: Cristina Menghini 

from Index_lib import *
from collections import OrderedDict

def Memory_PostList(postingsfile):
# This function creates in memory the posting lists of the various terms read from postingsfile.
#- postingsfile is the name(string), and eventyally the path, of the text file that contains the postings list('postings.txt')
    with open(postingsfile) as f:
        post = [line.strip().split('\t') for line in f]
    memory_post = {x[0]: x[1:] for x in post}
    posting_memory = OrderedDict(sorted(memory_post.items(), key = lambda y: int(y[0])))
    return posting_memory

def MapOfTerms(vocfile, postingMem):
# This function creates in memory a map of terms to posting lists, read from vocabulary.txt,
#- vocfile is the name of vocabulary file: 'vocabulary.txt';
#- postingMem is the return of Memory_PostList function
    with open(vocfile,'r+') as f:
        voc = [line.strip().split('\t') for line in f]
    memory_voc = {x[0]: x[1] for x in voc}
    memory_voc_ordered = OrderedDict(sorted(memory_voc.items(), key = lambda y: int(y[0])))
    vocab_memory = zip(memory_voc_ordered.values(), postingMem.values())
    voc_in_mem = {x[0]: x[1] for x in vocab_memory}
    voc_in_mem_ord = OrderedDict(sorted(voc_in_mem.items(), key = lambda y: y[0]))
    return voc_in_mem_ord


def AnsToQuery(processedquery, vocmem):
# This function returns the list of documents that contains the query.
#- processed query is the query preprocessed that is the return of Stemming(query).
#- vocmem is the MapOfTermFunction"""
    if len(processedquery) == 0:
        return None
    query = [q for q in processedquery if q in vocmem]
    if len(query) != len(processedquery):
        return None
    else:
        list_postings = [vocmem[processedquery[i]] for i in range(len(processedquery))]
        return Intersection(list_postings)

def Intersection(x):
    if len(x) == 1:
        return x[0]
    else:
        pointers = [0 for i in range(len(x))] # creation of pointers
        intersection = []
        while True:
            try:
                elems_pointed = [int(x[l][i]) for l,i in enumerate(pointers)]
                if len(set(elems_pointed)) == 1: # se tutti gli elementi estratti dai puntatori sono uguali
                    intersection.append(elems_pointed[0])
                    pointers = [pointers[i]+1 for i in range(len(x))]
                else: 
                    minimum = min(elems_pointed)
                    index = [i for i, v in enumerate(elems_pointed) if v == minimum]
                    for i in index:
                        pointers[i] = pointers[i]+1
            except:
                break
        return intersection


def AnsToUser(document_big, ansquery):
# This function prints the result of the query entered by the user.
#- document_big is the directory in which are stored the subdir of files;
#- ansquery is the rusult of AnsToQuery function.
    if len(ansquery) == 0:
        print 'It\'s impossible to find any advertisement that match your query.'
    else:
        list_sub_sort = sorted(os.listdir(document_big))[:]
        endpoints_list = []
        for dirs in list_sub_sort:
            split_dir = dirs.split('-')       
            endpoints_list.append(split_dir[1:])
        for i in [int(x) for x in ansquery]:
            for j in range(len(endpoints_list)):
                if i in range(int(endpoints_list[j][0]), int(endpoints_list[j][1])+1):
                    with open(document_big+'/documents-'+endpoints_list[j][0]+'-'+endpoints_list[j][1]+'/documents-'+'0'*(6-len(str(i)))+str(i),'r+') as f:
                        info = f.read().split('\t')
                        print '\n'.join(info[0:4])
                        print '--------------------------------------------------------------------'
                    break
