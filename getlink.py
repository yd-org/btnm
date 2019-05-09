import requests, json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
}
def getlink(link):
    data = {
        'link': link,
    }
    resp = requests.post("https://tool.lu/urlconvert/ajax.html", headers = headers, data= data)
    text = resp.text.encode('utf-8').decode('unicode_escape')
    text = json.loads(text, encoding='utf-8')
    httplink = text['text']['http']
    return httplink
