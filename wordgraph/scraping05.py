
### TITLE    電気新聞デジタル (scraping05)
### VARSION  v1.0   2017/12/16  初版  Y.K
# coding: utf-8

import requests
import re
from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime

#/接続先HP 電気新聞デジタル/
domain = "https://www.denkishimbun.com"

#/ニューストピックス階層 ※ものによってはこの階層に記事無し/
startpath = ""

basesoup = BeautifulSoup(requests.get(domain + startpath).text, "lxml")
#print(basesoup)

links = []

#/不必要な情報も取ってしまうため、正規表現には注意/
for a in basesoup.find_all("a", href=re.compile("/archives/[0-9\._?+-]")):

    links.append(a.get("href"))

links = list(set(links))
#print(links)

texts = []
count = 0

for link in links:
    #/焦らず急ごう/
    sleep(2)
    #/ただリストで回すだけ/
    soup = BeautifulSoup(requests.get(link).text, "lxml")
    #/h1で検索してね/
    title = soup.find("h1", class_="detail_news_topics").text.strip()
    #/h1近くの記事(日本語名が書かれている箇所)近くのdiv class=""の値を設定/
    main = soup.find("div", class_="news_text").text.strip() 
    #/以下おまじない(html形式のごみを消し、書き込んでいるだけ)/
    text = (title + " " + main).replace("\u3000"," ")
    text = text.replace("\r","")
    text = text.replace("\n","")
    text = text.replace("\xa0","")

    texts.append(text)
    #print(text)

    count = count + 1

    #print (datetime.now().isoformat()+":("+str(count)+"/"+str(len(links))+")")


#/↓↓ここからが謎↓↓/
import sqlite3
import hashlib

dbname = "text_denki.db"
dbcon = sqlite3.connect(dbname)
dbcur = dbcon.cursor()

for text in texts:

    insert = "INSERT INTO rawtext(id, source, time, rawtext) VALUES(?, ?, ?, ?)"

    id = hashlib.md5(text.encode("utf-8")).hexdigest()

    source = "電気新聞デジタル"

    time = datetime.now().isoformat()

    args = (id, source, time, text)

    try:

        dbcur.execute(insert, args)

    except sqlite3.Error as e:

        print('sqlite3:', e.args[0])

dbcon.commit()

dbcon.close()

print (datetime.now().isoformat()+":db written")

