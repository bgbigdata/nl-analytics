
# coding: utf-8

# In[22]:


import requests
import re
from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime

domain = "http://jp.techcrunch.com"
startpath = "/"

basesoup = BeautifulSoup(requests.get(domain + startpath).text, "lxml")

links = []
for a in basesoup.find_all("a", href=re.compile("/[0-9][0-9]")):
    links.append(a.get("href"))

links = list(set(links))



texts = []
count = 0

for link in links:
    sleep(2)
    res = requests.get(link)
    soup = BeautifulSoup(requests.get(link).text, "lxml")
    title = soup.find("h1", class_="alpha tweet-title").text.strip()
    main = "".join([x.text.strip() for x in soup.find_all("p")])

    text = (title + " " + main).replace("\u3000"," ")
    #/改善したい↓
    text = text.replace("!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+'://platform.twitter.com/widgets.js';fjs.parentNode.insertBefore(js,fjs);}}(document, 'script', 'twitter-wjs');タレコミ・寄稿お待ちしています！新着記事を毎日配信しますメールマガジンには広告が含まれる場合や、TechCrunchのイベント関連情報などをお送りさせていただく場合もあります。 個人情報保護方針新着記事を毎日配信しますメールマガジンには広告が含まれる場合や、TechCrunchのイベント関連情報などをお送りさせていただく場合もあります。 個人情報保護方針","")
    text = text.replace("原文","")
    text = text.replace("翻訳","")   
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
    source = "techcrunch"
    time = datetime.now().isoformat()
    
    args = (id, source, time, text)
    
    try:
        dbcur.execute(insert, args)
    except sqlite3.Error as e:
        print('sqlite3:', e.args[0])
    
dbcon.commit()
dbcon.close()
print (datetime.now().isoformat()+":db written")

