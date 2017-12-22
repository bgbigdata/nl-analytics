
# coding: utf-8

# In[4]:


### TITLE    産経ニュース (scraping10)

### VARSION  v1.0   2017/12/21  初版  Y.I




# coding: utf-8



import requests

import re

from time import sleep

from bs4 import BeautifulSoup

from datetime import datetime



domain = "http://www.sankei.com"



startpath = ""



basesoup = BeautifulSoup(requests.get(domain + startpath).text, "lxml")

#print(basesoup)



links = []



for a in basesoup.find_all("a", href=re.compile("/economy/news/[a-zA-Z0-9\._?+-]")):



    links.append(domain + a.get("href"))



links = list(set(links))

#print(links)

texts = []

count = 0



for link in links:

    sleep(2)

    soup = BeautifulSoup(requests.get(link).text, "lxml")

    title = soup.find("h1").text.strip()

    main = soup.find("div", class_="fontMiddiumText").text.strip()
    
    text = (title + " " + main).replace("\u3000"," ")
    
    if text.find("http") != -1:
        continue
    
    #URL拾っちゃってるので消したい。。。

    text = text.replace("\r","")

    text = text.replace("\n","")

    text = text.replace("\xa0","")

    texts.append(text)
    


    count = count + 1

    print (datetime.now().isoformat()+":("+str(count)+"/"+str(len(links))+")")

import sqlite3

import hashlib



dbname = "text.db"

dbcon = sqlite3.connect(dbname)

dbcur = dbcon.cursor()



for text in texts:



 

    insert = "INSERT INTO rawtext(id, source, time, rawtext) VALUES(?, ?, ?, ?)"

    id = hashlib.md5(text.encode("utf-8")).hexdigest()

    source = "産経ニュース"

    time = datetime.now().isoformat()

    args = (id, source, time, text)




    try:

        dbcur.execute(insert, args)

    except sqlite3.Error as e:

        print('sqlite3:', e.args[0])



dbcon.commit()

dbcon.close()



print (datetime.now().isoformat()+":db written")

