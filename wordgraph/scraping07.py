### TITLE    ���t�H�[���Y�ƐV��(scraping07)
### VARSION  v1.0   2017/12/16  ����  Y.K

# coding: utf-8

import requests
import re
import urllib
from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime

#/�ڑ���HP ���t�H�[���Y�ƐV��/
target_url = 'http://www.reform-online.jp'

html = urllib.request.urlopen(target_url).read()

basesoup = BeautifulSoup(html, "lxml")
#print(basesoup)

links = []

#/�s�K�v�ȏ�������Ă��܂����߁A���K�\���ɂ͒���/
for a in basesoup.find_all("a", href=re.compile("/news/[a-zA-Z]*/[a-zA-Z0-9\._?+-]")):

    links.append(target_url + a.get("href"))

links = list(set(links))
print(links)

texts = []
count = 0

for link in links:
    #/�ł炸�}����/
    sleep(2)
    #/�������X�g�ŉ񂷂���/
    soup = BeautifulSoup(requests.get(link).text, "lxml")
    #/h1���������I�I/
    title = soup.find("h1").text.strip()
    #/h1�߂��̋L��(���{�ꖼ��������Ă���ӏ�)�߂���div class=""�̒l��ݒ�/
    main = soup.find("div", class_="postArea").text.strip() 
    #/�ȉ����܂��Ȃ�(html�`���̂��݂������A��������ł��邾��)/
    text = (title + " " + main).replace("\u3000"," ")
    text = text.replace("\r","")
    text = text.replace("\n","")
    text = text.replace("\xa0","")

    texts.append(text)
    print(text)

    count = count + 1

    print (datetime.now().isoformat()+":("+str(count)+"/"+str(len(links))+")")


#/�����������炪�䁫��/
import sqlite3
import hashlib

dbname = "text_denki.db"
dbcon = sqlite3.connect(dbname)
dbcur = dbcon.cursor()

for text in texts:

    insert = "INSERT INTO rawtext(id, source, time, rawtext) VALUES(?, ?, ?, ?)"

    id = hashlib.md5(text.encode("utf-8")).hexdigest()

    source = "���t�H�[���Y�ƐV��"

    time = datetime.now().isoformat()

    args = (id, source, time, text)

    try:

        dbcur.execute(insert, args)

    except sqlite3.Error as e:

        print('sqlite3:', e.args[0])

dbcon.commit()

dbcon.close()

print (datetime.now().isoformat()+":db written")

