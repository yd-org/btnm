from dbtool import getconn

def likedata(key):
    conn = getconn()
    cursor = conn.cursor()
    #cursor.callproc('SEARCH',(key,))
    cursor.execute('SELECT TOP 10 KEYWORD FROM dbo.BT_KEYWORDS WHERE FREETEXT(KEYWORD,%s) ORDER BY NEWID()',key)
    datas = list(cursor)
    conn.close()
    return datas

