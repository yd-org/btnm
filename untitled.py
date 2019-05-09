from flask import Flask,request, redirect, url_for, session
from flask import render_template
from music import Musicdownload
from pager import Pagination
import base64, re, movie, youku, jiami
from btgetkeys import btgetkeys
from btlike import likedata

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysession'
    
@app.route('/')
def index():
    keys = btgetkeys()
    return render_template('index.html',keys = keys)

@app.route('/mobile/index')
def mindex():
    keys = btgetkeys()
    return render_template('mobile/index.html',keys = keys)

@app.route('/resume/index')
def resume():
    return render_template('resume.html')

@app.route('/bt/yunbo')
def yunbo():
    yburl = request.args.get("id")
    moviename = request.args.get("moviename")
    if yburl in ['',None]:
        return render_template('404.html')
    else:
        return render_template('yunbo.html',link = yburl, moviename = moviename)

@app.route('/mobile/yunbo')
def myunbo():
    yburl = request.args.get("id")
    moviename = request.args.get("moviename")
    if yburl in ['',None]:
        return render_template('404.html')
    else:
        return render_template('mobile/yunbo.html',link = yburl, moviename = moviename)

@app.route('/suggest')
def suggest():
    import json
    re_datas = []
    key = request.args.get("s")
    if key in ["", None]:
        return json.dumps(re_datas, ensure_ascii=False)
    else:
        re_datas = likedata(key)
        return json.dumps(re_datas, ensure_ascii=False)

@app.route('/user')
def user():
    user = session.get('username')
    if not user:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('music'))

@app.route('/reg',methods=["POST","GET"])
def reg():
    if request.method == "GET":
        return render_template('reg.html')
    else:       
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        subject = request.form['subject']
        message = request.form['message']
        if name.strip() == "" or len(name) > 10 or password.strip() == "" or len(password) < 6 or password != subject:
            return render_template('regfail.html')
        else:
            from dbtool import getconn
            conn = getconn()
            cursor = conn.cursor()
            cursor.callproc('USERREG',(name,email,password,message,))
            res = list(cursor)[0][0]
            conn.close()
            if res == '1':
                return render_template('regsuccess.html')
            else:
                return render_template('reg.html',content="用户名已存在，请换一个！")
        
@app.route('/login',methods=["POST","GET"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        loginname = request.form['name']
        loginpassword = request.form['password']
        from dbtool import getconn
        conn = getconn()
        cursor = conn.cursor()
        cursor.callproc('USERLOGIN',(loginname,loginpassword,))
        loginres = list(cursor)[0][0]
        conn.close()
        if loginres == '0':
            return render_template('loginfail.html')
        else:
            mdl = request.form.get('cs')
            session['username'] = loginname
            if mdl == "mdl":
                session.permanent = True
            return render_template('loginsuccess.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/bt/help')
def help():
    return render_template('help.html')

@app.route('/bt',methods=["POST","GET"])
def bt():
    from datetime import datetime
    from bt import api, keyword
    from pager1 import Pagination1
    from dbtool import getconn
    key = request.args.get('search')
    page = request.args.get('page')
    key = re.sub('[\s\)\(\,\"\?\？]','',key)
    if page == None:
        if key not in ["",None] and key not in keyword and len(key) >= 2:
            conn = getconn()
            cursor = conn.cursor()
            try:
                cursor.callproc("BTKEYINSERT",(key,))
            finally:
                conn.close()
    if page in ["",None,"0"]:
        page=1
    if key in ["",None]:
        key = "dota"
    result = api(key,page)
    contents = result[0]
    if contents != 0:
        contents = list(map(lambda x:(jiami.base64encode(x[0]),jiami.base64encode(x[1]),x[2],x[3],x[4],x[5],x[1][0:60]),contents))
    total = int(result[1])
    if request.method == "POST":
        url = "./bt?search="+key
    else:
        url = "./bt?"
    bt_obj = Pagination1(page,total,url,request.args,per_page_count=30)
    html = bt_obj.page_html()
    likedatas = likedata(key)
    if len(likedatas) == 0:
        likedatas = [(key,)]
    return render_template('bt.html', res = contents, key = key, html = html, likedatas = likedatas)

@app.route('/mobile/bt',methods=["POST","GET"])
def mbt():
    from bt import api, keyword
    from dbtool import getconn
    key = request.args.get('search')
    key = re.sub('[\s\)\(\,\"\?\？]','',key)
    if key in ["",None]:
        key = "dota"
    result = api(key,1)
    contents = result[0]
    if contents != 0:
        contents = list(map(lambda x:(jiami.base64encode(x[0]),jiami.base64encode(x[1]),x[2],x[3],x[4],x[5],x[1]),contents))
    likedatas = likedata(key)
    if len(likedatas) == 0:
        likedatas = [(key,)]
    return render_template('mobile/bt.html',res = contents, likedatas = likedatas, key = key)
    

@app.route('/bt/download')
def btdownload():
    import jieba
    dictags = []
    id = request.args.get('id')
    title = request.args.get('title')
    title = re.sub('\s','+',title)
    id = jiami.base64decode(id)
    title = jiami.base64decode(title)
    tags = list(jieba.cut_for_search(title))
    tags = list(map(lambda x:x if len(x)>=2 else '',tags))
    for tag in tags:
        if tag not in dictags:
            dictags.append(tag)
    return render_template('btdownload.html',id = id, title = title, tags = dictags)

@app.route('/mobile/download')
def mbtdownload():
    import jieba
    dictags = []
    id = request.args.get('id')
    title = request.args.get('title')
    title = re.sub('\s','+',title)
    id = jiami.base64decode(id)
    title = jiami.base64decode(title)
    tags = list(jieba.cut_for_search(title))
    tags = list(map(lambda x:x if len(x)>=2 else '',tags))
    for tag in tags:
        if tag not in dictags:
            dictags.append(tag)
    return render_template('mobile/btdownload.html',id = id, title = title, tags = dictags)   

@app.route('/joke')
def joke():
    import datetime
    jokelists = []
    flag = None
    timenow = str(datetime.datetime.now())[0:10]
    from dbtool import getconn
    conn = getconn()
    cursor = conn.cursor()
    cursor.callproc('WZSEARCH')
    results = list(cursor)
    conn.close()
    for result in results:
        title = result[0]
        time = result[1][0:16]
        time1 = result[1][0:10]
        time2 = time1.replace('-','')
        if timenow == time1:
            flag = "1"
        else:
            flag = "0"
        content = result[2]
        jokelists.append((title, content, time, flag, time1, time2))
    pager_obj = Pagination(request.args.get("page",1),len(jokelists),request.path,request.args,per_page_count=12)
    index_list = jokelists[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    return render_template('joke.html', index_list=index_list, html = html)

@app.route('/joke/detail')
def jokedetaile():
    number = 0
    detailelists = []
    date = request.args.get('date')
    qs = request.args.get('qs')
    from dbtool import getconn
    conn = getconn()
    cursor = conn.cursor()
    cursor.callproc('WZDETAILSEARCH',(date,))
    detaileresults = list(cursor)
    conn.close()    
    for detaileresult in detaileresults:
        title = detaileresult[0]
        time = detaileresult[2][0:16]
        content = detaileresult[1].split(',')
        number = number + 1
        detailelists.append((title, content, time, number))
    return render_template('/joke/detaile.html',contents = detailelists, titles = qs)

@app.route('/wzinsert')
def wzinsert():
    lb = request.args.get('lb')
    title = request.args.get('title')
    content = request.args.get('content')
    if lb != None:
        from dbtool import getconn
        conn = getconn()
        cursor = conn.cursor()
        cursor.callproc('WZINSERT',(lb,title,content,))
        conn.close()
        return redirect(url_for('wzinsert'))
    return render_template('wzinsert.html')

@app.route('/btxxinsert')
def btxxinsert():
    btid = request.args.get('btid')
    title = request.args.get('title')
    size = request.args.get('size')
    day = request.args.get('day')
    hits = request.args.get('hits')
    yburl = request.args.get('yburl')
    if btid != None:
        from dbtool import getconn
        conn = getconn()
        cursor = conn.cursor()
        cursor.callproc('BTXXINSERT',(btid,title,size,day,hits,yburl,))
        conn.close()
        return redirect(url_for('btxxinsert'))
    return render_template('btxxinsert.html')

@app.route('/about')
def about():
    return render_template('about.html')
	
@app.route('/cg')
def cg():
    return render_template('cg.html')
	
@app.route('/music',methods=["POST","GET"])
def music():
    flag = None
    songinput = request.args.get('songinput')
    if songinput == None or songinput == "":
        flag = "n"
        return render_template("music.html",flag=flag)
    else:
        songlist = None
        if songinput == "新歌推荐":
            from getnewmusic import getnewmusic
            res = getnewmusic()
            songs = []
            n = 1
            for re in res:
                songname = re[0][0:30]
                time = re[2]
                hash = re[1]
                id = re[3]
                hash = base64.encodebytes(bytes(hash, 'utf-8'))
                id = base64.encodebytes(bytes(str(id), 'utf-8'))
                hash = str(hash).replace("b'", '').replace(r"\n'", '')
                id = str(id).replace("b'", '').replace(r"\n'", '')
                songs.append((n, songname, '未知', time, hash, id))
                n += 1
            return render_template("music.html",flag=flag, total = 96, context=songs, key = songinput, page = 1)
        else:
            from pager1 import Pagination1
            page = request.args.get('page')
            if page in [None,"","0"]:
                page = 1
            url = "./music?"
            md = Musicdownload(songinput, page)
            songlist = md.run()
            songs = songlist[0]
            total = songlist[1]
            music_obj = Pagination1(page,total,url,request.args,per_page_count=30)
            html = music_obj.page_html()
            return render_template("music.html",flag=flag, total = total, context=songs, key = songinput, html = html, page = page)

@app.route('/freemovie/api')
def jiexi():
    url = request.args.get('key')
    inwordkey = ['黄色电影','av','AV','av电影','AV电影','苍井空','无码','小泽玛利亚','武藤兰','无码av','无码AV','av无码','AV无码','苍井空无码','无码苍井空','波多野结衣','大沢佑香','小泉彩','原田明绘','色情电影','做爱']
    if url not in ["",None] and url not in inwordkey:
        if "//" not in url and "www" not in url and ".com" not in url:
            from dbtool import getconn
            conn = getconn()
            cursor = conn.cursor()
            cursor.callproc("VDKEYINSERT",(url,))
            conn.close()
    content = youku.youku(url)
    flag = content[1]
    if flag == "no":
        return "电影 "+url+" 暂时还不存在，请联系管理员。"
    else:
        return render_template("./freemovieol/jiexi.html",context=content)

@app.route('/music/download')
def parase_url():
    user = session.get('username')
    if user:
        hash = request.args.get('code')
        id = request.args.get('sid')
        hash = base64.decodebytes(bytes(hash, 'utf-8'))
        id = base64.decodebytes(bytes(id, 'utf-8'))
        hash = (str(hash).replace("b'", '')).replace("'", '')
        id = (str(id).replace("b'", '')).replace("'", '')
        md= Musicdownload()
        download = md.download_url(hash,id)
        download_url = download[0]
        img = download[1]
        lyrics = download[2]
        title = download[3]
        ablum = download[4]
        return render_template("music/index.html",context=(title,download_url, ablum, img, lyrics))
    else:
        return render_template("nologin.html")

@app.route('/juanzeng')
def juanzeng():
    return render_template("juanzeng.html")
    
@app.route('/freemovie')
def freemovie():
    content = movie.getdata()[0]
    content1 = movie.getdata()[1]
    content2 = movie.getdata()[2]
    movieaddr = request.args.get('url')
    from vdgetkeys import vdgetkeys
    vdkeys = vdgetkeys()
    return render_template("freemovieol.html",context=movieaddr, contents=content, contents1=content1, contents2=content2, vdkeys = vdkeys)
	
@app.route('/nologin')
def nologin():
    return render_template("nologin.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('404.html'),500

@app.context_processor
def myprocessor():
    username = session.get('username')
    if username:
        return {'user': username}
    return {}
	
if __name__ == '__main__':
    app.run()
