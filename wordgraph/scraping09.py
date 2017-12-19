
# coding: utf-8

# In[1]:


### TITLE    交通新聞
### VARSION  v1.0   2017/12/16  初版  H.Y

import requests
import re
import sqlite3
import hashlib

from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime

domain = "http://www.kotsu.co.jp"
startpath = "/topics/"

basesoup = BeautifulSoup(requests.get(domain + startpath).text, "lxml")

links = []
for a in basesoup.find_all("a", href=re.compile("/index.php?.*")):
    target_url = domain + a.get("href")
    links.append(target_url)
    
texts = []
#count = 0

for link in links:
    sleep(2)
    soup = BeautifulSoup(requests.get(link).text, "lxml")
    rawtext = soup.find("div", class_="detailBlock").text.strip()
    texts.append(rawtext)
    
    #count = count + 1
    #print (datetime.now().isoformat()+":("+str(count)+"/"+str(len(links))+")")

#print(texts[0])

dbname = "text.db"
dbcon = sqlite3.connect(dbname)
dbcur = dbcon.cursor()

for text in texts:
    insert = "INSERT INTO rawtext(id, source, time, rawtext) VALUES(?, ?, ?, ?)"

    id = hashlib.md5(text.encode("utf-8")).hexdigest()
    source = "交通新聞"
    time = datetime.now().isoformat()
    args = (id, source, time, text)

    try:
        dbcur.execute(insert, args)
    except sqlite3.Error as e:
        print('sqlite3:', e.args[0])

dbcon.commit()
dbcon.close()

