import pymssql

def getconn():
    conn = pymssql.connect(server="localhost", user="sa", password="huanqiu_888", database="CDDFUN", autocommit=True)
    return conn
