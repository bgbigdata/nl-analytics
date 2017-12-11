
# coding: utf-8

# In[3]:


import requests
import re
from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime

domain = "https://senken.co.jp"
startpath = "/categories/general"

basesoup = BeautifulSoup(requests.get(domain + startpath).text, "lxml")


# In[9]:


links = []
for a in basesoup.find_all("a", href=re.compile("/posts/[a-zA-Z0-9\._¥+-]")):
    links.append(domain + a.get("href"))
links = list(set(links))

print(links)


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

