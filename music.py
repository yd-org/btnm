import  requests, re, json ,base64

class Musicdownload(object):
    base_url = "http://songsearch.kugou.com/song_search_v2?callback=jQuery112407507331082826529_1536909176399" \
               "&keyword={}&page={}&pagesize=30&userid=-1&clientver=" \
               "&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0&_=1536909176401"
    down_url = "http://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery191046558493281196833_1536907165442" \
              "&hash={}&album_id={}&_=1536907165443"
    headers = {
        'User-Agent':"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0"
    }
    #初始化对象
    def __init__(self,songname=None,page=None):
        self.songname = songname
        #定义歌曲序号
        self.n = 1
        #定义歌曲序号列表
        self.nlist = []
        self.page = page

    #音乐下载程序入口
    def run(self):
        songlist = self._parase_page(self.base_url.format(self.songname, self.page))
        return songlist
    #解析歌曲搜索页面
    def _parase_page(self,url):
        sonlist = []
        respons = requests.get(url,headers=self.headers)
        text = respons.content.decode('utf-8')
        rel_text = text.replace("jQuery112407507331082826529_1536909176399(",'').replace(")",'')
        list_text = json.loads(rel_text,encoding='utf-8')
        total = list_text["data"]["total"]
        dicitem = list_text["data"]["lists"]
        for dic in dicitem:
            self.nlist.append(str(self.n))
            title = dic['FileName']
            hash = base64.encodebytes(bytes(dic['FileHash'], 'utf-8'))
            id = base64.encodebytes(bytes(dic['AlbumID'], 'utf-8'))
            hash = str(hash).replace("b'", '').replace(r"\n'", '')
            id = str(id).replace("b'", '').replace(r"\n'", '')
            duration = dic['Duration']
            seconds = duration % 60
            if seconds == "0":
                seconds = "00"
            if 0 < seconds < 10:
                seconds = "0"+str(seconds)
            AlbumName = "《"+re.sub('[<em> | </em>]','',dic['AlbumName'])+"》"
            if len(AlbumName) > 20:
                AlbumName = AlbumName[0:20]+'...'
            if dic['AlbumID'] == "":
                AlbumName = "未知"
            title = re.sub('[<em> | </em>]', '', title)
            if len(title) > 25:
                title = title[0:25]+'...'
            songdic = (self.n,title,AlbumName,str(duration // 60)+":"+str(seconds),hash,id)
            sonlist.append(songdic)
            self.n += 1
        return (sonlist,total)
    #解析歌曲地址
    def download_url(self,request_hash,request_id):
        url = self.down_url.format(request_hash,request_id)
        respons = requests.get(url,headers=self.headers)
        text = respons.text
        result = text.replace("jQuery191046558493281196833_1536907165442(", "").replace(');', "")
        js_result = json.loads(result, encoding='utf-8')
        lyrics = js_result['data']['lyrics']
        lyrics = lyrics.split("\r\n")
        img = js_result['data']['img']
        download_url = js_result['data']['play_url']#歌曲地址
        audio_name = js_result['data']['audio_name']
        album_name = js_result['data']['album_name']
        return (download_url, img, lyrics, audio_name, album_name)
