from dbtool import getconn

def btgetkeys():
    conn = getconn()
    cursor = conn.cursor()
    #cursor.callproc('SEARCHTOP')
    cursor.execute('SELECT TOP 30 SUBSTRING(KEYWORD,1,10),[COUNT] FROM dbo.BT_KEYWORDS ORDER BY [COUNT] DESC')
    keys = list(cursor)
    conn.close()
    return keys

