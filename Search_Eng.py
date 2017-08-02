# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 18:14:34 2015

@author: fisheryzhq
"""

import re

file_url = "/Users/fisheryzhq/Desktop/CS609Data Mgt&Explore on Web/Web_Spider_Data/my_index_bool.txt"
doc_position = "/Users/fisheryzhq/Desktop/CS609Data Mgt&Explore on Web/Web_Spider_Data/map.txt"

#Read Posting
bool_index_file = open(file_url, 'r').read()

doc_url_file = open(doc_position, 'r').read()

list_bool = bool_index_file.split('\n')

doc_url = doc_url_file.split('\n')

query = ["worth", "work", "woman"]
# For this query we should output in this order:
# 1. appear and appl
# 2. appear or appl

#First, in order to use RE, should + "\W" to each item in query
query_bool = ["work", "worth", "woman"]
for i in range(0, len(query)):
    query_bool[i] = query_bool[i] + "\W"


def get_doc_url(doc_num):
    print "len %d" % len(doc_num)
    for i in range(0, len(doc_num)):
        doc = "Doc" + str(doc_num[i]) + "\D"
        #print doc
        for j in enumerate(doc_url):
            if(re.match(doc, j[1])):
                print j[1]

#1. appear and appl

#store the term and doc num
found_term_list = []

#Find the term in the index
for i in range(0, len(query)):
    for j in enumerate(list_bool):
        if(re.match(query_bool[i], j[1])):
            found_term_list.append(j[1].split('['))
            break

# If no term is found, return error!
if(len(found_term_list) == 0):
    print "Term is not finded!"
    exit()

temp = []
for i in enumerate(found_term_list):
    temp.append(i[1][1].split(']'))

doc_list = []
for i in enumerate(temp):
    doc_list.append(i[1][0].split(', '))
    
# If there is just one term, output all document that contain the term
if(len(found_term_list) == 1):
    get_doc_url(doc_list[0])

#print cmp(int("15"), int("2"))

#Search for condition "and"
start_cmp = doc_list[0]
temp = []
for i in range(1, len(doc_list)):
    for j in range(0, len(start_cmp)):
        for k in range(0, len(doc_list[i])):
            #print start_cmp[j]
            #print doc_list[i][k]
            if(cmp(start_cmp[j], doc_list[i][k]) == 0):
                temp.append(start_cmp[j])
                break
            if(cmp(int(start_cmp[j]), int(doc_list[i][k])) < 0):
                break
    start_cmp = []
    start_cmp = temp
    if(len(temp) == 0):
        break
    temp = []



print "#################################################"
print "#########   Simple Boolean  #####################"
print "#################################################\n"
if(len(start_cmp) == 0):
    print "No and condition for those terms!"
else:
    get_doc_url(start_cmp)



#2. appear or appl
# For this, we should eliminate those doc have already in 1.
OrCondition = set()

#for i in enumerate(start_cmp):
   # OrCondition.add(i[1])

for i in range(0, len(doc_list)):
    for j in range(0, len(doc_list[i])):
        OrCondition.add(doc_list[i][j])

#print OrCondition

Or_list = list(OrCondition - set(start_cmp))

if(len(Or_list) != 0):
    get_doc_url(Or_list)


#######################
# Vector Space
########################
import math as ma

vec_url = "/Users/fisheryzhq/Desktop/CS609Data Mgt&Explore on Web/Web_Spider_Data/my_index_vec.txt"

vec_index = open(vec_url, 'r').read().split('\n')

found_term_list = []

for i in enumerate(vec_index):
    found_term_list.append(i[1].split('['))
    
temp = []
for i in enumerate(found_term_list):
    temp.append(i[1][1].split('), ('))

idf = []
for i in range(0, len(temp)):
    idf.append(ma.log10(100/len(temp[i])))


#print temp[0][0].split(', ')[1]

TF_IDF = {}

for i in range(0, len(temp)):
    tf_idf = []
    for j in range(0, len(temp[i])):
        #Find tf
        ex = temp[i][j].split(', ')[1]
        if(ex.find(')]') != -1):
            tf = int(ex.split(')')[0])
        else:
            tf = int(ex)
        #Find cooresponding doc#
        exn = temp[i][j].split(', ')[0]
        if(exn.find('(') != -1):
            #print exn.split('(')[1]
            n_doc = int(exn.split('(')[1])
        else:
            n_doc = int(exn)
        tf_idf.append((n_doc, tf*idf[i]))
    TF_IDF[found_term_list[i][0]] = tf_idf

vec_doc = {}

for i in TF_IDF:
    #print i
    for j in range(0, len(TF_IDF[i])):
        #print TF_IDF[i][j]
        if(vec_doc.has_key(TF_IDF[i][j][0])):
            vec_doc[TF_IDF[i][j][0]].append(TF_IDF[i][j][1])
        else:
            vec_doc[TF_IDF[i][j][0]] = [TF_IDF[i][j][1]]

#Calculate doc length
length_doc = {}

for i in vec_doc:
    sum_square = 0.0
    for j in range(0, len(vec_doc[i])):
        sum_square = sum_square + ma.pow(vec_doc[i][j], 2)
    length_doc[i] = ma.sqrt(sum_square)
        
#deal with query

query_vec = []
for i in range(0, len(query)):
    if(TF_IDF.has_key(query[i])):
        query_vec.append(TF_IDF[query[i]])

query_tf_idf = {}

for i in range(0, len(query_vec)):
    for j in range(0, len(query_vec[i])):
        if(query_tf_idf.has_key(query_vec[i][j][0])):
            query_tf_idf[query_vec[i][j][0]] = query_tf_idf[query_vec[i][j][0]] + query_vec[i][j][1]
        else:
            query_tf_idf[query_vec[i][j][0]] = query_vec[i][j][1]

#divide by length of doc
for i in query_tf_idf:
    if(length_doc.has_key(i)):
        query_tf_idf[i] = query_tf_idf[i]/length_doc[i]
    else:
        print "Document Number Error!!"

# Rank the result
import operator
Rank_result = sorted(query_tf_idf.items(), key=operator.itemgetter(1), reverse = True)
#print Rank_result

rank_vec = []
for i in range(0, len(Rank_result)):
    rank_vec.append(Rank_result[i][0])

print "\n\n\n"
print "#################################################"
print "#########   Vector Space    #####################"
print "#################################################\n"
get_doc_url(rank_vec)
    
    
    
    