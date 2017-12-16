### TITLE    �l���V�� (scraping06)
### VARSION  v1.0   2017/12/16  ����  Y.K

# coding: utf-8

import requests
import re
from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime

#/�ڑ���HP �l���V��/
domain = "https://www.shikoku-np.co.jp"

#/�j���[�X�g�s�b�N�X�K�w �����̂ɂ���Ă͂��̊K�w�ɋL������/
startpath = ""

basesoup = BeautifulSoup(requests.get(domain + startpath).text, "lxml")
#print(basesoup)

links = []

#/�s�K�v�ȏ�������Ă��܂����߁A���K�\���ɂ͒���/
for a in basesoup.find_all("a", href=re.compile("/national/main/[0-9\._?+-]")):

    links.append(domain + a.get("href"))

for a in basesoup.find_all("a", href=re.compile("/national/social/[0-9\._?+-]")):

    links.append(domain + a.get("href"))

for a in basesoup.find_all("a", href=re.compile("/national/economy/[0-9\._?+-]")):

    links.append(domain + a.get("href"))

for a in basesoup.find_all("a", href=re.compile("/national/political/[0-9\._?+-]")):

    links.append(domain + a.get("href"))

for a in basesoup.find_all("a", href=re.compile("/national/international/[0-9\._?+-]")):

    links.append(domain + a.get("href"))

for a in basesoup.find_all("a", href=re.compile("/national/life_topic/[0-9\._?+-]")):

    links.append(domain + a.get("href"))

for a in basesoup.find_all("a", href=re.compile("/national/culture_entertainment/[0-9\._?+-]")):

    links.append(domain + a.get("href"))

for a in basesoup.find_all("a", href=re.compile("/national/science_environmental/[0-9\._?+-]")):

    links.append(domain + a.get("href"))

for a in basesoup.find_all("a", href=re.compile("/national/medical_health/[0-9\._?+-]")):

    links.append(domain + a.get("href"))

links = list(set(links))
#print(links)

texts = []
count = 0

for link in links:
    #/�ł炸�}����/
    sleep(2)
    #/�������X�g�ŉ񂷂���/
    soup = BeautifulSoup(requests.get(link).text, "lxml")
    #/���̃T�C�g��h1��class�ł͂Ȃ�id�ݒ肾����/
    title = soup.find("div", class_="Articletitle").text.strip()
    #/h1�߂��̋L��(���{�ꖼ��������Ă���ӏ�)�߂���div class=""�̒l��ݒ�/
    main = soup.find("div", class_="articlemain").text.strip() 
    #/�ȉ����܂��Ȃ�(html�`���̂��݂������A��������ł��邾��)/
    text = (title + " " + main).replace("\u3000"," ")
    text = text.replace("\r","")
    text = text.replace("\n","")
    text = text.replace("\xa0","")

    texts.append(text)
    #print(text)

    count = count + 1

    #print (datetime.now().isoformat()+":("+str(count)+"/"+str(len(links))+")")


#/�����������炪�䁫��/
import sqlite3
import hashlib

dbname = "text_denki.db"
dbcon = sqlite3.connect(dbname)
dbcur = dbcon.cursor()

for text in texts:

    insert = "INSERT INTO rawtext(id, source, time, rawtext) VALUES(?, ?, ?, ?)"

    id = hashlib.md5(text.encode("utf-8")).hexdigest()

    source = "�l���V��"

    time = datetime.now().isoformat()

    args = (id, source, time, text)

    try:

        dbcur.execute(insert, args)

    except sqlite3.Error as e:

        print('sqlite3:', e.args[0])

dbcon.commit()

dbcon.close()

print (datetime.now().isoformat()+":db written")

