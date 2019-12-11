import pymysql


def get_keyword():
    db = pymysql.connect(host="", user="", passwd="", db="ai_intelligence")
    cursor = db.cursor()
    cursor.execute("SELECT cnKeyword from datacrawl_searchkeyword where (typeId LIKE '8;%' OR typeId LIKE '%;8;%' OR typeId LIKE '%;8' OR typeId = '8')")
    keyword = cursor.fetchall()
    db.close()
    return keyword

