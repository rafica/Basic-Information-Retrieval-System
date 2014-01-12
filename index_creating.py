"""
Creates inverted index file with a dictionary of stemmed words with their exact location in all the documents
Creates a file with a dictionary named processeddict with title, author and other parts separated under each document
Creates a file with dictionary named uncategorized_wordlist with list of words under each document

How to use:
1.Input the file path eg. C:\Python27\CranField
2.After the index creation a message is displayed "Index Created"
3.Run the search.py file to input the query

"""
import time
import os,sys
import re
import time
import operator
from xml.dom.minidom import parse
import string
import nltk
import pickle
#import xml.etree.ElementTree as ET

filepath = raw_input('Enter the file path')
#filelist = os.listdir("C:\\Python27\\CranField")
filelist = os.listdir(filepath)
categorized_doc={}

stopwords = ['a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also', 'am', 'among', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'but', 'by', 'can', 'cannot', 'could', 'dear', 'did', 'do', 'does', 'either', 'else', 'ever', 'every', 'for', 'from', 'get', 'got', 'had', 'has', 'have', 'he', 'her', 'hers', 'him', 'his', 'how', 'however', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'just', 'least', 'let', 'like', 'likely', 'may', 'me', 'might', 'most', 'must', 'my', 'neither', 'no', 'nor', 'not', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our', 'own', 'rather', 'said', 'say', 'says', 'she', 'should', 'since', 'so', 'some', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas', 'us', 'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'would', 'yet', 'you', 'your']

processeddict={}  ################## for retrieving the title or author directly using document number ########################
inverted_index={}   ################## inverted index ############################
uncategorized_wordlist={} ############## list of all words with document number as key ############################



def punc_remove(str):
    for c in string.punctuation:
        str=str.replace(c," ")
    return str
def newline_remove(str):
    str=str.replace("\n"," ")
    return str

def punc_remove_query(str):
    for c in string.punctuation:
        str = str.replace(c,"")
    return str
def union_list(a,b):
    return list(set(a)|set(b))

def union_dictionary(a ,b):
    result={}
    if len(a.keys())>0:
        key_a = a.keys()
    elif len(a.keys())==0:
        key_a = []
            
    if len(b.keys())>0:
        key_b = b.keys()
    elif len(b.keys())==0:
        key_b = []
    
    key_union = union_list(key_a, key_b)
    for key in key_union:
        if key in a and key in b:
            result[key]=union_list(a[key],b[key])
        elif key in a:
            result[key]=a[key]
        elif key in b:
            result[key]=b[key]

    return result


x = nltk.porter.PorterStemmer()

labellist=['DOCNO','TITLE','AUTHOR','BIBLIO','TEXT']
docnum = 1

start = time.time()
print "timer starts"

for filex in filelist:
    #dom = parse("C:\\Python27\\CranField\\"+filex)
    dom = parse(filepath+"\\"+filex)
    pos = 0
    uncategorized_wordlist[docnum]=[]
    for label in labellist:
        
        
        #parse and add to dictionary
        
        labelnode = dom.getElementsByTagName(label)
     
        categorized_doc[label] =str(newline_remove(labelnode[0].firstChild.nodeValue))

        
        processed_words = nltk.word_tokenize(str((newline_remove(punc_remove(labelnode[0].firstChild.nodeValue))).decode('utf8')))
       
        uncategorized_wordlist[docnum].extend(processed_words) # all words indexed and categorized into documents
        #remove stop words
        filtered_list= [w for w in processed_words if not w in stopwords]
        for wordx in processed_words:
              
              word = x.stem(wordx)
              
              
              if word not in inverted_index:
                  inverted_index[word]={}
              dic = inverted_index[word]
            
              if not(dic.has_key(docnum)):
                  dic[docnum]=[]
              poslist=dic[docnum]
              poslist.append(pos)
          
              dic[docnum]=poslist
      
              inverted_index[word] = dic
              pos = pos+1
        processeddict[docnum]=categorized_doc
       
        
    docnum =docnum+1
    categorized_doc={}

pickle.dump(inverted_index, open("index.txt", "wb"))
pickle.dump(uncategorized_wordlist, open("wordlist.txt", "wb"))
pickle.dump(processeddict,open("easy_retrieval.txt", "wb"))


print "Index created"

print "Total words in the index is %d " % len(inverted_index)

print "It took ",time.time()- start, "seconds"

#statinfo = os.stat('index_creating.py')

print "Size of the inverted index file is " + str(os.path.getsize('index_creating.py'))+"kb"
            
        
