from dbtool import getconn

def getdata():
    conn = getconn()
    cursor = conn.cursor()
    cursor.callproc('GETMOVIES')
    res = list(cursor)
    conn.close()
    datas = []
    datas1 = []
    datas2 = []
    for re in res:
        if re[4] == '1':
            datas.append(re)
        elif re[4] == '2':
            datas1.append(re)
        else:
            datas2.append(re)
    return (datas, datas1, datas2)
