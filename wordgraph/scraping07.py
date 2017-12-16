### TITLE    リフォーム産業新聞(scraping07)
### VARSION  v1.0   2017/12/16  初版  Y.K

# coding: utf-8

import requests
import re
import urllib
from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime

#/接続先HP リフォーム産業新聞/
target_url = 'http://www.reform-online.jp'

html = urllib.request.urlopen(target_url).read()

basesoup = BeautifulSoup(html, "lxml")
#print(basesoup)

links = []

#/不必要な情報も取ってしまうため、正規表現には注意/
for a in basesoup.find_all("a", href=re.compile("/news/[a-zA-Z]*/[a-zA-Z0-9\._?+-]")):

    links.append(target_url + a.get("href"))

links = list(set(links))
print(links)

texts = []
count = 0

for link in links:
    #/焦らず急ごう/
    sleep(2)
    #/ただリストで回すだけ/
    soup = BeautifulSoup(requests.get(link).text, "lxml")
    #/h1だけ抜く！！/
    title = soup.find("h1").text.strip()
    #/h1近くの記事(日本語名が書かれている箇所)近くのdiv class=""の値を設定/
    main = soup.find("div", class_="postArea").text.strip() 
    #/以下おまじない(html形式のごみを消し、書き込んでいるだけ)/
    text = (title + " " + main).replace("\u3000"," ")
    text = text.replace("\r","")
    text = text.replace("\n","")
    text = text.replace("\xa0","")

    texts.append(text)
    print(text)

    count = count + 1

    print (datetime.now().isoformat()+":("+str(count)+"/"+str(len(links))+")")


#/↓↓ここからが謎↓↓/
import sqlite3
import hashlib

dbname = "text_denki.db"
dbcon = sqlite3.connect(dbname)
dbcur = dbcon.cursor()

for text in texts:

    insert = "INSERT INTO rawtext(id, source, time, rawtext) VALUES(?, ?, ?, ?)"

    id = hashlib.md5(text.encode("utf-8")).hexdigest()

    source = "リフォーム産業新聞"

    time = datetime.now().isoformat()

    args = (id, source, time, text)

    try:

        dbcur.execute(insert, args)

    except sqlite3.Error as e:

        print('sqlite3:', e.args[0])

dbcon.commit()

dbcon.close()

print (datetime.now().isoformat()+":db written")

