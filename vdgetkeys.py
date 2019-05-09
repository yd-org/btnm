from dbtool import getconn

def vdgetkeys():
    conn = getconn()
    cursor = conn.cursor()
    cursor.callproc('VDSEARCH')
    vdkeys = list(cursor)
    conn.close()
    return vdkeys