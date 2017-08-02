# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 09:16:06 2015

@author: xichao
"""
import web
import os

render = web.template.render('')
urls = ('/', 'sh',)
app = web.application(urls,globals()) 
class sh:
    def GET(self):
     return render.sh() 
     
    def POST(self):
        f=file("url_pages.txt","w+")
        f2=file("query.txt","w+")
        
        form=web.input()
        url=form.urlSH
        Pages=form.pages
        Ordinary_url=url
        KeyWords=form.keywordSH      

        f.writelines(Ordinary_url+"\n")
        f.writelines(Pages)
        f2.writelines(KeyWords)
        f.close()
        f2.close()
        
        os.system("python Crawler.py")
        os.system("python Indexing.py")
        #os.system("python Search_Eng.py") 
        
        return "Crawling and Indexing Done!"

if __name__ == '__main__':
    app.run()
    
