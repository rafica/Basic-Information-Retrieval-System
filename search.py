"""
What it does?
1. Inputs the query
2. Preprocesses it
3. Displays the results with snippets 

How to use?
1. Run this file
2. Input the query. phrases should be enclosed by double quotes. if you dont want documents with a particular word , the syntax of the query should be !word
3. Type :q to quit



Additional features:
1.for the query ->   author 123
 author of the document number 123 will be returned

2.The output results display document number and all the snippers containing the query words. Top 25 results are displayed

3.boundary-layer is considered as boundary layer


"""
import os
import re
import time
import operator
from xml.dom.minidom import parse
import string
import nltk
import cPickle as pickle
from sys import exit
#import xml.etree.ElementTree as ET
filelist = os.listdir("C:\\Python27\\CranField")
processeddict={}
categorized_doc={}
inverted_index={}
rank_list={}

uncategorized_wordlist={}

stopwords = ['a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also', 'am', 'among', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'but', 'by', 'can', 'cannot', 'could', 'dear', 'did', 'do', 'does', 'either', 'else', 'ever', 'every', 'for', 'from', 'get', 'got', 'had', 'has', 'have', 'he', 'her', 'hers', 'him', 'his', 'how', 'however', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'just', 'least', 'let', 'like', 'likely', 'may', 'me', 'might', 'most', 'must', 'my', 'neither', 'no', 'nor', 'not', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our', 'own', 'rather', 'said', 'say', 'says', 'she', 'should', 'since', 'so', 'some', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas', 'us', 'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'would', 'yet', 'you', 'your']
def query_extraction(query1):
    phrase_list1=[]
    phrase1=[]
    not_list1=[]
    not_phrase_list1=[]
    plain1=[]
    word_list1 = str.split(query1)
    phrase_flag=0
    not_flag=0
    i=1
    for word1 in word_list1:
        i = i+1
        if phrase_flag != 1:
            if word1[0]=='!':
                not_flag=1
                if word1[1]!='"':
                    not_list1.append(punc_remove_query(word1))
                    not_flag=0
                    continue
       
            
            if (not_flag!=1 and word1[0]=='"')or (not_flag==1 and word1[1]=='"'):
                phrase_flag =1

            if not_flag!=1 and phrase_flag!=1:
                plain1.append(punc_remove_query(word1))
                continue
                
        if phrase_flag==1:
            
            phrase1.append(punc_remove_query(word1))   
            if word1[len(word1)-1]=='"':
                phrase_flag=0
                
            if phrase_flag==0:
                if not_flag==1:
                    not_phrase_list1.append(phrase1)
                    not_flag=0
                else:
                    phrase_list1.append(phrase1)
                phrase1 = []
         
    return (phrase_list1,not_list1,not_phrase_list1,plain1)




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


inverted_index = pickle.load(open("index.txt", "rb"))
processeddict= pickle.load(open("easy_retrieval.txt", "rb"))
uncategorized_wordlist= pickle.load(open("wordlist.txt", "rb"))

                             
                            


            
        
        


###################input query#############################

inputflag=1
while(inputflag==1):
    print "Enter :q to quit"
    query = raw_input('enter the query')
    if query == ":q":
        break
    
    

    start = time.time()

    split_words = query.split()
    if split_words[0]=="title":
        doc_id_q = int(split_words[1])
        index_quick = processeddict[doc_id_q]
        print index_quick["TITLE"]
        exit(0)
    elif split_words[0]=="author":
        doc_id_q = int(split_words[1])
        index_quick = processeddict[doc_id_q]
        print index_quick["AUTHOR"]
        exit(0)
    elif split_words[0]=="doc":
        doc_id_q = int(split_words[1])
        index_quick = processeddict[doc_id_q]
        print index_quick["TEXT"]
        exit(0)
    elif split_words[0]=="df":
        term = split_words[1]
        if term[0]!='"':
            term = x.stem(term)
            if term in inverted_index:
                doc_freq= len(inverted_index[term])
                print doc_freq
                exit(0)
        elif term[0]=='"':
            phrase_join= query[2+2:-1]
            phrase_join =punc_remove(phrase_join)
            phrase = phrase_join.split()
            phrase_position ={}
            pplist =[]
            first_word = phrase[0]
            first_word = x.stem(first_word)
            if first_word in inverted_index:
                
                doc_list_pos = inverted_index[first_word]
                doc_list = doc_list_pos.keys()
                for doc in doc_list:
                    
                    #print doc_list_pos[doc]
                    for pos_num in doc_list_pos[doc]:
                        t_pos_num = pos_num
                        i = 1
                        first_list=uncategorized_wordlist[doc]
                        while i<len(phrase) and t_pos_num<len(first_list)-1 and first_list[t_pos_num+1] == phrase[i]:
                            #print "in while.yayy"
                            i = i+1
                            t_pos_num=t_pos_num+1
                            if i == len(phrase):
                                if pplist:
                                    pplist[0]=pos_num
                                else:
                                    pplist.append(pos_num)
                                
                                phrase_position[doc] = pplist
                               
                        pplist=[]
            print len(phrase_position)
            exit(0)

    elif split_words[0]=="freq":
        term = split_words[1]
        freq =0
        if term[0]!='"':
            term = punc_remove(term)
            if x.stem(term) in inverted_index:
                pos_dict = inverted_index[x.stem(term)]
            for doc in pos_dict:
                freq = freq + len(pos_dict[doc])
            print freq
            exit(0)
        elif term[0]=='"':
            phrase_join = query[4+2:-1]
            phrase_join = punc_remove(phrase_join)
            phrase = phrase_join.split()
            first_word = phrase[0]
            first_word = x.stem(first_word)
            if first_word in inverted_index:
                
                doc_list_pos = inverted_index[first_word]
                doc_list = doc_list_pos.keys()
                for doc in doc_list:
                    
                    #print doc_list_pos[doc]
                    for pos_num in doc_list_pos[doc]:
                        t_pos_num = pos_num
                        i = 1
                        first_list=uncategorized_wordlist[doc]
                        while i<len(phrase) and t_pos_num<len(first_list)-1 and first_list[t_pos_num+1] == phrase[i]:
                            #print "in while.yayy"
                            i = i+1
                            t_pos_num=t_pos_num+1
                            if i == len(phrase):
                                freq = freq+1
                            

            print freq
            exit(0)
    elif split_words[0]=="tf":
        tf = 0
        doc_id = split_words[1]
        term = split_words[2]
        if term[0]!='"':
            term = punc_remove(term)
            if x.stem(term) in inverted_index:
                pos_dic = inverted_index[x.stem(term)]
                if int(doc_id) in pos_dic:
                    print len(pos_dic[int(doc_id)])
                    exit(0)
                else:
                    print 0
                    exit(0)
        elif term[0]=='"':
            phrase_join = query[2+len(doc_id)+3:-1]
            phrase_join = punc_remove(phrase_join)
            phrase = phrase_join.split()
            first_word = phrase[0]
            first_word = x.stem(first_word)
            if first_word in inverted_index:
                doc_list_pos = inverted_index[first_word]
                doc_list = doc_list_pos.keys()
                if int(doc_id) in doc_list:
                    #print "present"
                    for pos_num in doc_list_pos[int(doc_id)]:
                            t_pos_num = pos_num
                            i = 1
                            first_list=uncategorized_wordlist[int(doc_id)]
                            while i<len(phrase) and t_pos_num<len(first_list)-1 and first_list[t_pos_num+1] == phrase[i]:
                                #print "in while.yayy"
                                i = i+1
                                t_pos_num=t_pos_num+1
                                if i == len(phrase):
                                    tf = tf+1

            print tf
            exit(0)

    elif split_words[0]=="similar":
        term = split_words[1]
        sim_dic ={}
        length = len(term)
        for i in range(1,len(uncategorized_wordlist)):
            for word in uncategorized_wordlist[i]:
                if word not in sim_dic:
                    sim = nltk.edit_distance(term,word)
                    if sim!=0 and sim<length/2:
                        print word
                        sim_dic[word] = sim
                
        exit(0)
                    
            
            


    phrase_list,not_list,not_phrase_list,plain_list= query_extraction(query)

    #print phrase_list
    #print not_list
    #print not_phrase_list
    #print plain_list



    #################### PHRASE LIST ############################

    phrase_union={}
    pplist=[]
    phrase_position={}
    weight = {}
    if phrase_list:
        for phrase in phrase_list:
            first_word = phrase[0]
            first_word = x.stem(first_word)
            if first_word in inverted_index:
                doc_list_pos = inverted_index[first_word]
                doc_list = doc_list_pos.keys()
                for doc in doc_list:
                    for pos_num in doc_list_pos[doc]:
                        t_pos_num = pos_num
                        i = 1
                        first_list=uncategorized_wordlist[doc]
                        while i<len(phrase) and t_pos_num<len(first_list)-1 and first_list[t_pos_num+1] == phrase[i]:
                            i = i+1
                            t_pos_num=t_pos_num+1
                        if i == len(phrase):
                            if pplist:
                                pplist[0]=pos_num
                            else:
                                pplist.append(pos_num)
                            if doc not in weight:
                                weight[doc]=0
                            weight[doc] = weight[doc] + len(phrase)
                            phrase_position[doc] = pplist
                           
                    pplist=[]
                
            phrase_union = union_dictionary(phrase_union,phrase_position)            
                    
                       
        
    ############################ PLAIN WORDS ######################################

    words_query= [w for w in plain_list if not w in stopwords]


    doc_union = {}
    for word in words_query:
        word = x.stem(word)
        if word in inverted_index:
            doc_positions = inverted_index[word]
            doc_union = union_dictionary(doc_union,doc_positions)

         
    for doc in doc_union:
        if doc not in weight:
            weight[doc]=0
        weight[doc]=weight[doc]+len(doc_union[doc])
        
        

    #union of union ( PHRASES AND PLAIN WORDS )
    final_union = union_dictionary(phrase_union, doc_union)

    #print final_union

    ################### NOT WORDS ########################### 

    not_doc_list= [w for w in not_list if not w in stopwords]
    doc_not_positions = {}
    doc_positive_list = final_union.keys()
    doc_union = {}
    for word in not_doc_list:
        word = x.stem(word)
        if word in inverted_index:
            doc_not_positions = inverted_index[word]
            doc_not_list = doc_not_positions.keys()
            for i in range(1,len(uncategorized_wordlist)):
                if doc_positive_list:
                    if i not in doc_not_list and i in doc_positive_list:
                        weight[i]=weight[i]+1
                else:
                     if i not in doc_not_list:
                         if i not in weight:
                             weight[i] = 1
                         else:
                             weight[i] = weight[i]+1
                         final_union[i] = [len(uncategorized_wordlist[i])/2]


    not_phrase_position={}

    if not_phrase_list:
        for phrase in not_phrase_list:
            first_word = phrase[0]
            first_word = x.stem(first_word)
            if first_word in inverted_index:
                doc_not_list_pos = inverted_index[first_word]
                doc_not_list = doc_not_list_pos.keys()
                for doc in doc_not_list:
                    
                    for pos_num in doc_not_list_pos[doc]:
                        t_pos_num = pos_num
                        i = 1
                        first_list=uncategorized_wordlist[doc]
                        while i<len(phrase) and t_pos_num<len(first_list)-1 and first_list[t_pos_num+1] == phrase[i]:
                            #print "in while.yayy"
                            i = i+1
                            t_pos_num=t_pos_num+1
                        if i == len(phrase):
                            if pplist:
                                pplist[0]=pos_num
                            else:
                                pplist.append(pos_num)
                           
                            not_phrase_position[doc] = pplist
                            
                    pplist=[]
            for i in range(1,len(uncategorized_wordlist)):
                if doc_positive_list:
                    if i not in not_phrase_position and i in doc_positive_list:
                        weight[i] = weight[i] + len(phrase)
                else:
                    if i not in not_phrase_position:
                        if i not in weight:
                            weight[i] = len(phrase)
                        else:
                            weight[i] = weight[i] + len(phrase)
                        final_union[i] = [len(uncategorized_wordlist[i])/2]
                    


    ######################## RANKING #########################



    weight_tuple = weight.items()
    final_weight_list= sorted(weight_tuple, key= lambda weight_tuple:weight_tuple[1], reverse=True)




    #print final_weight_list


    #################### OUTPUT WITH SNIPPET #####################################
    result = 0
    for item in final_weight_list:
        if result==25:
            break
        doc_id = item[0]
        print "Document Number %d" % doc_id
        position_list = final_union[doc_id]
        total =len(uncategorized_wordlist[doc_id])
        for index_num in position_list:
            if index_num>1 and index_num<total-2:
               print "...."+uncategorized_wordlist[doc_id][index_num-2]+" "+uncategorized_wordlist[doc_id][index_num-1]+" "+uncategorized_wordlist[doc_id][index_num]+" "+uncategorized_wordlist[doc_id][index_num+1]+" "+uncategorized_wordlist[doc_id][index_num+2]+"..."
            elif index_num==0:
                print uncategorized_wordlist[doc_id][index_num]+" "+uncategorized_wordlist[doc_id][index_num+1]+" "+uncategorized_wordlist[doc_id][index_num+2]+"..."
            elif index_num==total-1:
                print "..."+uncategorized_wordlist[doc_id][index_num-2]+" "+uncategorized_wordlist[doc_id][index_num-1]+" "+uncategorized_wordlist[doc_id][index_num]
        print "--------------------------------------------"
        result = result + 1

    print "%d results (maximum limit 25)" % result
    print "Search results in ",time.time() - start, "seconds"
                  

        
    
    

    
