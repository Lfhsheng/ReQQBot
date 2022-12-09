import sqlite3
path = "./keywords.db"
def init():
    base = sqlite3.connect(path)
    cursor = base.cursor()
    cursor.execute('''CREATE TABLE KEYWORDS(
        KEYWORDS TEXT NOT NULL,
        WORD     TEXT NOT NULL
        );''')
    base.commit()
    base.close()
def addKeyWord(keyword,word):
    base = sqlite3.connect(path)
    cursor = base.cursor()
    try:
        cursor.execute('''INSERT INTO KEYWORDS (KEYWORDS,WORD) VALUES ("%s","%s");''' % (str(keyword),str(word)))
    except:
        init()
        cursor.execute('''INSERT INTO KEYWORDS (KEYWORDS,WORD) VALUES ("%s","%s");''' % (str(keyword),str(word)))
    base.commit()
    base.close()
def updateKeyWord(keyword,newword):
    base = sqlite3.connect(path)
    cursor = base.cursor()
    cursor.execute('''UPDATE KEYWORDS SET WORD = "%s" WHERE KEYWORDS = "%s"''' % (newword,keyword))
    base.commit()
    base.close()
def delKeyWord(keyword):
    base = sqlite3.connect(path)
    cursor = base.cursor()
    print(1)
    cursor.execute('''DELETE FROM KEYWORDS WHERE KEYWORDS = "%s"''' % keyword)
    base.commit()
    base.close()
def getData():
    base = sqlite3.connect(path)
    cursor = base.cursor()
    return cursor.execute("SELECT * from KEYWORDS").fetchall()
def seeData():
    base = sqlite3.connect(path)
    cursor = base.cursor()
    sqlResult = cursor.execute("SELECT * from KEYWORDS").fetchall()
    result = ""
    for keywords in sqlResult:
        result += "%s - %s\n" % (keywords[0],keywords[1])
    return result
def matchingKeyWord():
    base = sqlite3.connect(path)
    cursor = base.cursor()
    result = cursor.execute("SELECT * from KEYWORDS").fetchall()
    return result
if __name__ == "__main__":
    seeData()