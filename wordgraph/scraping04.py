
# coding: utf-8

# In[3]:


import requests
import re
from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime


domain = "https://senken.co.jp"
startpath1 = "/categories/general"
startpath2 = "/categories/corporation"
startpath3 = "/categories/hr"
startpath4 = "/categories/trend"
startpath5 = "/categories/product"
startpath6 = "/categories/startup"
startpath7 = "/categories/supply"
startpath8 = "/categories/education"
startpath9 = "/categories/sales"
startpath10 = "/categories/carrer"
startpath11 = "/categories/report"
startpath12 = "/categories/senkenjob"
startpath13 = "/categories/column"
startpath14 = "/categories/technical-terms"

basesoup1 = BeautifulSoup(requests.get(domain + startpath1).text, "lxml")
basesoup2 = BeautifulSoup(requests.get(domain + startpath2).text, "lxml")
basesoup3 = BeautifulSoup(requests.get(domain + startpath3).text, "lxml")
basesoup4 = BeautifulSoup(requests.get(domain + startpath4).text, "lxml")
basesoup5 = BeautifulSoup(requests.get(domain + startpath5).text, "lxml")
basesoup6 = BeautifulSoup(requests.get(domain + startpath6).text, "lxml")
basesoup7 = BeautifulSoup(requests.get(domain + startpath7).text, "lxml")
basesoup8 = BeautifulSoup(requests.get(domain + startpath8).text, "lxml")
basesoup9 = BeautifulSoup(requests.get(domain + startpath9).text, "lxml")
basesoup10 = BeautifulSoup(requests.get(domain + startpath10).text, "lxml")
basesoup11 = BeautifulSoup(requests.get(domain + startpath11).text, "lxml")
basesoup12 = BeautifulSoup(requests.get(domain + startpath12).text, "lxml")
basesoup13 = BeautifulSoup(requests.get(domain + startpath13).text, "lxml")
basesoup14 = BeautifulSoup(requests.get(domain + startpath14).text, "lxml")
# In[9]:

cleansing = "/posts/[a-zA-Z0-9\._¥+-][a-zA-Z0-9\._¥+-][a-zA-Z0-9\._¥+-]"
links = []
for a in basesoup1.find_all("a", href=re.compile(cleansing)):
    links.append(domain + a.get("href"))
for a in basesoup2.find_all("a", href=re.compile(cleansing)):
    links.append(domain + a.get("href"))
for a in basesoup3.find_all("a", href=re.compile(cleansing)):
    links.append(domain + a.get("href"))
for a in basesoup4.find_all("a", href=re.compile(cleansing)):
    links.append(domain + a.get("href"))
for a in basesoup5.find_all("a", href=re.compile(cleansing)):
    links.append(domain + a.get("href"))
for a in basesoup6.find_all("a", href=re.compile(cleansing)):
    links.append(domain + a.get("href"))
for a in basesoup7.find_all("a", href=re.compile(cleansing)):
    links.append(domain + a.get("href"))
for a in basesoup8.find_all("a", href=re.compile(cleansing)):
    links.append(domain + a.get("href"))
for a in basesoup9.find_all("a", href=re.compile(cleansing)):
    links.append(domain + a.get("href"))
for a in basesoup10.find_all("a", href=re.compile(cleansing)):
    links.append(domain + a.get("href"))
for a in basesoup11.find_all("a", href=re.compile(cleansing)):
    links.append(domain + a.get("href"))
for a in basesoup12.find_all("a", href=re.compile(cleansing)):
    links.append(domain + a.get("href"))
for a in basesoup13.find_all("a", href=re.compile(cleansing)):
    links.append(domain + a.get("href"))
for a in basesoup14.find_all("a", href=re.compile(cleansing)):
    links.append(domain + a.get("href"))
links = list(set(links))


#print(links)


# In[15]:



texts = []
count = 0

for link in links:
    sleep(2)
    soup = BeautifulSoup(requests.get(link).text, "lxml")
    title = soup.find("h1", class_="m-b-1").text.strip()
    main = soup.find("div", class_="article-content m-y-2").text.strip() 
    text = (title + " " + main).replace("\u3000"," ")
    text = text.replace("\r","")
    text = text.replace("\n","")
    text = text.replace("\xa0","")
    texts.append(text)
    count = count + 1
    print (datetime.now().isoformat()+":("+str(count)+"/"+str(len(links))+")")


# In[16]:


import sqlite3
import hashlib

dbname = "text.db"
dbcon = sqlite3.connect(dbname)
dbcur = dbcon.cursor()

for text in texts:
    insert = "INSERT INTO rawtext(id, source, time, rawtext) VALUES(?, ?, ?, ?)"

    id = hashlib.md5(text.encode("utf-8")).hexdigest()
    source = "繊研新聞"
    time = datetime.now().isoformat()
    
    args = (id, source, time, text)
    
    try:
        dbcur.execute(insert, args)
    except sqlite3.Error as e:
        print('sqlite3:', e.args[0])
    
dbcon.commit()
dbcon.close()
print (datetime.now().isoformat()+":db written")

