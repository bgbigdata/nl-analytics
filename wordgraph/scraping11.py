
# coding: utf-8

# In[15]:


# coding: utf-8 


# In[7]: 




import requests 
import re 
from time import sleep 
from bs4 import BeautifulSoup 
from datetime import datetime 


domain = "https://www.yakuji.co.jp" 
startpath = "/entrycategory/6" 

# In[8]: 


basesoup = BeautifulSoup(requests.get(domain + startpath).text, "lxml") 


# In[9]: 


links = [] 
for a in basesoup.find_all("a", href=re.compile("/entry[0-9]+.html")): 
    links.append(a.get("href")) 
    
# In[10]: 


texts = [] 
count = 0 


for link in links: 
    sleep(2) 
    soup = BeautifulSoup(requests.get(link).text, "lxml") 
    texts.append(soup.find("div", class_="title").text.strip() + " " + soup.find("div", class_="text").text.strip()) 
     
    count = count + 1 
    print (datetime.now().isoformat()+":("+str(count)+"/"+str(len(links))+")") 
    print (texts)
    


# In[ ]:


# In[6]: 




import sqlite3 
import hashlib 


dbname = "text.db" 
dbcon = sqlite3.connect(dbname) 
dbcur = dbcon.cursor() 


for text in texts: 
    insert = "INSERT INTO rawtext(id, source, time, rawtext) VALUES(?, ?, ?, ?)" 


    id = hashlib.md5(text.encode("utf-8")).hexdigest() 
    source = "薬事日報" 
    time = datetime.now().isoformat() 
     
    args = (id, source, time, text) 
     
    try: 
        dbcur.execute(insert, args) 
    except sqlite3.Error as e: 
        print('sqlite3:', e.args[0]) 
     
dbcon.commit() 
dbcon.close() 
print (datetime.now().isoformat()+":db written") 

