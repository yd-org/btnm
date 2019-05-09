import requests, re

def youku(moviename):
    url = moviename
    title = None
    if "//" in url:
        if url == "//":
            title,url = init()
        else:
            url = url.split('?')[0]
            title = parase(url)        
    elif url.strip() == "":
        title,url = init()
    else:
        if ".com" and "www." in url:
            title = moviename
        else:
            from getmovieurl import getmovieurl
            newurl = getmovieurl(moviename)
            title = moviename
            if newurl == "NOURL":
                response = requests.get("https://so.youku.com/search_video/q_{}".format(url))
                text = response.text
                text = text.replace('\\', '')
                title = re.findall(r'<h2 class="spc-lv-1">.*?<a.*?title="(.*?)".*?</a>', text, re.DOTALL)[0]
                url = re.findall(r'<div class="mod-left">.*?<a.*?href="(.*?)".*?</a>', text, re.DOTALL)
                if len(url) == 0:
                    url = ""
                else:
                    url = url[0]
                    if "v.youku.com" not in url:
                        if "v.qq.com" in url:
                            pass
                        else:
                            url = parase_tencent(moviename)
            else:
                url = newurl
                
    return (title,url)


def parase(url):
    resp = requests.get(url)
    text = resp.text
    text = text.replace('\\', '')
    if "youku" in url:
        title = re.findall(r'<div class="tvinfo">.*?<a.*?>(.*?)</a>', text, re.DOTALL)[0]
    elif "iqiyi" in url:
        title = re.findall(r'<h1 class="player-title".*?>.*?<span.*?>(.*?)</span>', text, re.DOTALL)[0]
    elif "v.qq.com" in url:
        text1 = resp.content.decode('utf-8')
        text1 = text1.replace('\\', '')
        title = re.findall(r'<h2 class="player_title">.*?<a.*?>(.*?)</a>', text1, re.DOTALL)[0]
    elif "www.le.com" in url:
        title = re.findall(r'<div class="briefIntro_tit">.*?<a.*?>(.*?)</a>', text, re.DOTALL)[0]
    else:
        title = url
    return title

def parase_tencent(name):
    orig_url = "https://v.qq.com/x/search/?q={}".format(name)
    response = requests.get(orig_url)
    text = response.text
    url = re.findall(r'<div class="_infos">.*?<a href="(.*?)".*?</a>', text, re.DOTALL)
    if len(url) == 0:
        url = "no"
    else:
        url = url[0]
    if "detail" in url:
        resp = requests.get(url)
        content = resp.text
        url = re.findall(r'<div class="container_inner">.*?<a href="(.*?)".*?</a>', content, re.DOTALL)[0]
    return url

def init():
    lis = ('「DOTA伍声2009」大酒神精彩操作','http://www.iqiyi.com/w_19rrhqrvql.html')
    title = lis[0]
    url = lis[1]
    return (title,url)

