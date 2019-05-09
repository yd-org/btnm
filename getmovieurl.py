from dbtool import getconn

def getmovieurl(moviename):
    conn = getconn()
    cursor = conn.cursor()
    cursor.callproc('GETMOVIEURL',(moviename,))
    res = list(cursor)
    url = res[0][0]
    conn.close()
    return url