from dbtool import getconn

def getnewmusic():
    conn = getconn()
    cursor = conn.cursor()
    cursor.callproc('GETNEWMUSIC')
    res = list(cursor)
    conn.close()
    return res
