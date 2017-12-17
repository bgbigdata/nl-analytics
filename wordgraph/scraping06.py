### TITLE    四国新聞 (scraping06)
### VARSION  v1.0   2017/12/16  初版  Y.K
### VARSION  v1.1   2017/12/17  for文を1つに集約、DB書込みをアップグレード  Y.K

# coding: utf-8

import requests
import re
from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime

#/接続先HP 四国新聞/
domain = "https://www.shikoku-np.co.jp"

#/ニューストピックス階層 ※ものによってはこの階層に記事無し/
startpath = ""

basesoup = BeautifulSoup(requests.get(domain + startpath).text, "lxml")
#print(basesoup)

links = []

#/不必要な情報も取ってしまうため、正規表現には注意/
for a in basesoup.find_all("a", href=re.compile("/national/[a-zA-Z]*/[a-zA-Z0-9\._?+-]")):

    links.append(domain + a.get("href"))

links = list(set(links))
#print(links)

texts = []
count = 0

for link in links:
    #/焦らず急ごう/
    sleep(2)
    #/ただリストで回すだけ/
    soup = BeautifulSoup(requests.get(link).text, "lxml")
    #/このサイトはh1はclassではなくid設定だった/
    title = soup.find("h1").text.strip()
    #/h1近くの記事(日本語名が書かれている箇所)近くのdiv class=""の値を設定/
    main = soup.find("div", class_="articlemain").text.strip() 
    #/以下おまじない(html形式のごみを消し、書き込んでいるだけ)/
    text = (title + " " + main).replace("\u3000"," ")
    text = text.replace("\r","")
    text = text.replace("\n","")
    text = text.replace("\xa0","")

    texts.append(text)
    #print(text)

    count = count + 1

    print (datetime.now().isoformat()+":("+str(count)+"/"+str(len(links))+")")

#/↓↓ローカルにしか接続できないらしい↓↓/
#/①事前準備としてコマンドプロンプトでDBを作成
#/ cmd → sqlite3.exeへ移動 →「sqlite3 [DB名]」コマンドを実行/
#/②TABLEを作成/
#/「CREATE TABLE [テーブル名]([カラム1],[カラム2],…,[カラムx])」コマンドを実行)/
#/③TABLEが作成されていることを確認/
#/「.table」コマンドを実行)/

import sqlite3
import hashlib

dbname = "text.db"
dbcon = sqlite3.connect(dbname)
dbcur = dbcon.cursor()

for text in texts:

    #/コマンドや引数の値を定義/
    insert = "INSERT INTO scraping06(id, source, time, rawtext) VALUES(?, ?, ?, ?)"
    id = hashlib.md5(text.encode("utf-8")).hexdigest()
    source = "四国新聞"
    time = datetime.now().isoformat()
    args = (id, source, time, text)

    #/実行/
    try:
        dbcur.execute(insert, args)
    except sqlite3.Error as e:
        print('sqlite3:', e.args[0])

dbcon.commit()
dbcon.close()

print (datetime.now().isoformat()+":db written")
