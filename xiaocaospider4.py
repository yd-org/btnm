import requests, random, time, datetime
from lxml import etree
from dbtool import getconn
from xiaocaourl import xcurl

headers = {
    'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6821.400 QQBrowser/10.3.3040.400"
}
def geturls(url):
    resp = requests.get(url, headers=headers)
    text = resp.content.decode('gbk',errors='ignore')
    html = etree.HTML(text)
    if "4" in url:
        urls = html.xpath('//h3/a/@href')[5:]
    else:
        urls = html.xpath('//h3/a/@href')[3:]
    urls = list(map(lambda x:xcurl+x, urls))
    for url in urls:
        getbt(url)
        time.sleep(2)

def getbt(url):
    btid = None
    response = requests.get(url, headers=headers)
    text = response.content.decode('gbk',errors='ignore')
    html = etree.HTML(text)
    title = html.xpath('//h4/text()')
    if len(title) == 0:
        title = ""
    else:
        title = title[0]
    a_s = html.xpath('//a/text()')
    b_s = html.xpath('//a/@href')
    for a in a_s:
        if 'rmdown.com' in a:
            btid = a.split('=')[1].replace('191','')
        else:
            for b in b_s:
                if 'viidii.info' in b and '191' in b:
                    btid = b.split('=')
                    if len(btid) >= 2:
                        btid = btid[1].replace('191','').split('&')[0]
                    else:
                        btid = None
    hits = random.randint(0,1000)
    if btid != None:
        cursor.execute("""
        INSERT INTO BTXX(BTID,TITLE,SIZE,DAY,HITS) VALUES (%s,%s,%s,%s,%s)
        """, (btid, title, '未知', str(datetime.datetime.now())[0:10], hits))
conn = getconn()
cursor = conn.cursor()
urls = [xcurl+'thread0806.php?fid=15']
try:
    for url in urls:
        geturls(url)
finally:
    conn.close()

