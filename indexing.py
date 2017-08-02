# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 20:52:47 2015

@author: Nong
"""

import re
import os
import linecache
import sys
sys.path.append("/Users/Nong/Desktop/WSE_Proj")
import stemmer

path ="/Users/Nong/Desktop/WSE_Proj"
os.chdir(path)

#for mapping each link to each doc
index_map = "map.txt"
open(index_map,'w')

#compare 2 strings
def astrcmp(str1,str2):
    return str1==str2 

def stem(f):
    p = stemmer.PorterStemmer()
    
    infile = open(f, 'r')
    while 1:
        output = ''
        word = ''
        line = infile.readline()
        if line == '':
            break
        for c in line:
            if c.isalpha():
                word += c.lower()
            else:
                if word:
                    output += p.stem(word, 0,len(word)-1)
                    word = ''
                output += c.lower()
        #print output
        des_filename = "pre_stem.txt"
        open(des_filename,'w').writelines(output)
    infile.close() 

#do preprocess for Document{}.txt
#input: Document{}.txt
#output: pre_new.txt
def pre_file(filename, num):
    #print("Reading %r....."%filename)
    src_data = open(filename).read()
    link = linecache.getline(filename, 1)
    open(index_map,'at+').writelines("Doc"+str(num)+"\t"+link+"\n")
    link = re.sub(r'\?', '\\?', link)
    des_data = re.sub(link, '', src_data)
    des_data = re.sub(r'\/|\n+|_+', ' ', des_data)
    des_data = re.sub(r'，|。|、', ' ', des_data)
    des_data = re.sub(r',+|«|»|►|◄|¶|\||!|&+|\$|`|′|;|“|”|‘|’|·|©|~|↓|…|°|\'|"|#|₹|‹|›|″|×|†|•|←|→', '', des_data)
    des_data = re.sub(r'(http|https):\/\/', '', des_data)    
    des_data = re.sub(r'\(|\)|\{|\}|<|>|\[|\]', ' ', des_data)
    des_data = re.sub(r'\?+|\++|\*+|=+', ' ', des_data)
    des_data = re.sub(r'@|—', ' ', des_data)
    des_data = re.sub(r'\W+\.+|\.+\W+|\.\.+|\W+\-+|\-+\W+|\W+%|\W+:+|:+\W+', ' ', des_data)
    #regarding scripts & url
    des_data = re.sub(r'watchv\w*', ' ', des_data)
    des_data = re.sub(r'(position:[0-9]+)*url:(http|https):\\|position:[0-9]+item', ' ', des_data)
    des_data = re.sub(r'(www\.)*\w+\.(com|org|gov|jpg|gif|html)\\*', ' ', des_data)
    
    des_data = re.sub(r' +', ' ', des_data)
    des_data = re.sub(r'\xc2\xa0|\xe2\x80\x93|\xc3\x97|\xc2\x95|\xef\xbb\xbf', '', des_data)

    des_filename = "pre_new.txt"
    #print("Writing into%r....."%des_filename)
    open(des_filename,'w').writelines(des_data)
    #print("Preprocessing done!")
    #os.system("python stemmer.py pre_new.txt")
    stem("pre_new.txt")
    
#Input:test_new.txt
#Output:my_index.txt
def create_inverted_index(num):  
    #variable declaration
    word = []     #word list
    stop_w = []   #stopwords list
    result_b = {}   #output result for boolean {term:index}
    result_v = {}   #output result for vector {term:index}
    
    stop_w =[ line.rstrip() for line in open('stop_words.txt') ]

    #i for each number of doc
    for i in range(0, num+1):
        filename = "./Web_Spider_Data/Document"+ str(i) +".txt"
        #print("Reading file %r....."%filename)
        pre_file(filename, i)
        #each doc
        src_data = open('pre_stem.txt').read()
        
        sp_data = src_data.split()
        set_data = set(sp_data) #remove duplicates
        #set_data = sorted(set_data) #sort
    
        #removing stop-words
        temp = list(p for p in set_data if p not in stop_w)
        word = list(set(word + temp))
        #word = sorted(word)
        #print word
        
        sub_list = list(sp_data)
        sub_set = list(set_data)    #For boolean判断是否存在用的无重复子集

        #create index for term
        for w in range(0,len(word)):
            
            index_b = [] #recording doc [doc, doc,...]
            index_v = [] #recording doc and freq[(doc,fr),(doc,fr)...]
            
            # ———————————For boolean——————————— #
            #iterate through each word occurs in the doc
            for p in range(0,len(sub_set)):  
                if astrcmp(sub_set[p], word[w]):
                    if( result_b.has_key(word[w]) ):
                        result_b[word[w]].append(i)
                    else:
                        index_b.append(i)
                        result_b[word[w]] = index_b

            # ———————————For vector——————————— #
            fr = 0
            #iterate through each word in the doc
            for j in range(0,len(sub_list)):  
                if astrcmp(sub_list[j], word[w]):
                    fr += 1
            if(fr != 0):
                if( result_v.has_key(word[w]) ):
                    result_v[word[w]].append((i,fr))
                else:
                    index_v.append((i,fr))
                    result_v[word[w]] = index_v
        
    writebool = open("my_index_bool.txt",'w')
    writevec = open("my_index_vec.txt",'w')
    k_s = result_b.keys()
    k_s.sort()
    result_b = map(lambda key:(key,result_b[key]),k_s)
    result_v = map(lambda key:(key,result_v[key]),k_s)
    c = 0
    for k in k_s:
        writebool.writelines(str(k)+str(result_b[c][1])+"\n")
        writevec.writelines(str(k)+str(result_v[c][1])+"\n")
        c += 1 
    print("Indexing done!")
   

#Main function
def main():
    Pages = int(linecache.getline('url_pages.txt', 2))
    create_inverted_index(Pages)

#Run
if __name__ == '__main__':
    main()