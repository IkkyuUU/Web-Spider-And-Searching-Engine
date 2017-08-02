# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 19:44:52 2015

@author: fisheryzhq
"""

import requests
from pyquery import PyQuery as pq
import collections
import re
import codecs
import linecache

def get_url(url):
    "Gets the html content from the URL"
    return requests.get(url).content

p = re.compile(r'\/$')
st = linecache.getline('url_pages.txt', 1)
st = re.sub(r'\n', '', st)
if(p.search(st)):
    Ordinary_url = st
else:
    Ordinary_url = st+"/"
Adjust_url = Ordinary_url + "{}"
Pages = int(linecache.getline('url_pages.txt', 2))
#Ordinary_url = "http://www.foxnews.com/"
#Adjust_url = "http://www.foxnews.com/{}"
file_url = "/Users/fisheryzhq/Desktop/CS609Data Mgt&Explore on Web/Web_Spider_Data/Document{}.txt"

urls_queue = collections.deque()  
urls_queue.append(Ordinary_url)  
found_urls = set()  
found_urls.add(Ordinary_url)

def get_links(url):
    html = get_url(url)
    pqhtml = pq(html)
    # Links are from <a href="...", so we search for 'a' and get href if it exists
    all_links = [ a.attrib.get('href') for a in pqhtml('a') ]
    # Get all links  and put them in a set (removes duplicates)
    set_links = set([ link for link in all_links ])
    return set_links

def get_content(url, step):
    pqhtml = pq(get_url(url))
    f = codecs.open(file_url.format(step), 'w', 'utf-8-sig')
    f.write(url)
    f.write("\n")
    f.write(pqhtml('title').text())
    f.write("\n")
    f.write(pqhtml('a').text())
    f.write("\n")
    f.write(pqhtml('p').text())
    f.write("\n")
    f.write(pqhtml('ul').text())
    f.close

def check_urls_connection(url):
    try:
        requests.get(url, timeout=1.0)
        print "GET!"
        return True
    except requests.exceptions.RequestException, e:
        print "Error"
        print e
        return False

step = 0
totalNumber = 0
while(step <= Pages):
    # head_flag 是否需要加本网址的前部 0：need, 1: already have
    if(len(urls_queue) <= 0):
        break
    totalNumber = totalNumber + 1
    head_flag = 0
    print "Step: %d" % step
    url = urls_queue.popleft()
    print url
    if(url.find('../')>= 0):
        print "Already handled!!"
        continue
    if(re.search('http://', url) or re.search('https://', url)):
        head_flag = 1
    if(head_flag == 0):
        url = Adjust_url.format(url)
    if(re.search('/#', url) or re.search('#', url)):
        print "Duplicate！！！"
        continue
    if(check_urls_connection(url) == False):
        continue
    #get content
    get_content(url, step)
    
    level_links = get_links(url)

     # Set difference to find new URLs
    for link in (level_links - found_urls):
        found_urls.add(link)
        urls_queue.append(link)    
    
    step = step + 1
   
print totalNumber
print len(urls_queue)