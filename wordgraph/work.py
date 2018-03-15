import sqlite3

import unicodedata
from datetime import datetime
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
import pandas
from textblob import TextBlob

#dbtext = sqlite3.connect("file:text.db", uri=True)
#dbtext.row_factory = sqlite3.Row

dbword = sqlite3.connect("file:words.db", uri=True)
dbword.row_factory = sqlite3.Row

dbname = "text.db"
dbcon = sqlite3.connect(dbname)
dbcur = dbcon.cursor()

lasttime = ""
row = dbword.execute("select time from wordstbl order by time desc limit 1").fetchone()
if row is not None:
        lasttime = row["time"]

count = 0
fromtime = ""
totime = ""
separated_text = ""

for row in dbcur.execute("SELECT * FROM rawtext2 where time > ? order by time", (lasttime,)):
#    tag = nltk.pos_tag(nltk.word_tokenize(row[3]))
#
#    for u in range(len(tag)):
#            if ("NN" in tag[u][1]) or ("NNS" in tag[u][1]) or ("NNP" in tag[u][1]):
#                    separated_text = separated_text + " " +tag[u][0]
    print(row[3])
    txt = row[3]
    blob = TextBlob(txt)
    print(blob.noun_phrases)                    
    phrases = blob.noun_phrases
    for u in range(len(phrases)):
        separated_text = separated_text + " " +phrases[u]
    print(separated_text)

    insert = "INSERT INTO wordstbl(id, source, time, words) VALUES(?, ?, ?, ?)"
    args = (row[0], row[1], row[2], separated_text)

    if fromtime > row[2] or fromtime == "":
        fromtime = row[2]
    if totime < row[2]:
        totime = row[2]

#    try:
#        dbword.execute(insert, args)
#    except sqlite3.Error as e:
#        print ('sqlite3:', e.args[0])
    separated_text = ""

dbword.commit()
dbword.close()
dbcur.close()

print (datetime.now().isoformat()+":words.db written(" + str(count) + ")(" + fromtime + "~" + totime + ")")
