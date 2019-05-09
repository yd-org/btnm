import requests ,json
from dbtool import getconn

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
}
baseurl = "http://api.xhub.cn/api.php?op=search_list&callback=jQuery191017984181955718603_1543829841888&key={}&page={}"
keyword = ['无码片','处女膜','潮吹','习近平','JJ','jj','颜射','爆乳','巨乳','颜值','摸奶','奶门','大奶','骚货','包皮','色情','黑木耳','成都','宾馆','风骚','风骚少妇','离婚少妇','我','肏我','痴男','痴女','双飞','64','口活','3P','3p','性感尤物','性感','尤物','性爱','精子','精液','人妻','范冰冰','大保健','王老板','吉泽明步','广州','深喉','小鸟酱','狗爷','妇女','会所','内裤哥','东莞桑拿','桑拿','东莞','幼童','幼','幼女','日本','女同','群交','奴','军人','调教','欧美','国产','呵呵','军人','护士','高清无码','av女优','女优','无码中出','中出无码','中出','大桥未久','大橋未久无码','大橋未久','自慰','撸管','骚穴','小穴','呻吟','抽插','内射无套','无套内射','无套','无毛白虎逼','白虎逼','无毛白虎','白虎','无毛','黄色','露出','迷奸','幼奸','诱奸','处女','小穴','A片','a片','麻生希','人兽','兽交','幼女','幼童','酒井法子','足交','性交','乳交','小仓优子','肉体','捆绑','草逼','操逼','三级片','黄色电影','松岛枫','黄片','羽田爱','橘美穗','松下桃香','麻仓优','早乙女露依','雨宫琴音','友田彩也香','柚木提娜','橘梨纱','天海翼','私处','肉棒','天使萌','内射无码','内射','一本道无码','东京热无码','一本道','东京热','草榴社區','草榴社区','草榴','樱井莉亚无码','樱井莉亚','爆菊','口交','饭岛爱','桃谷绘里香','偷拍','SM','sm','黄色电影','av','AV','av电影','AV电影','苍井空','无码','小泽玛利亚','武藤兰','无码av','无码AV','av无码','AV无码','苍井空无码','无码苍井空','波多野结衣','大沢佑香','小泉彩','原田明绘','色情电影','做爱']

def api(key,page):
    dic = []
    conn = getconn()
    cursor = conn.cursor()
    try:
        cursor.callproc('GETBTXX',(page,key,))
        listre = list(cursor)
        listretotal = listre[0][4]
    finally:
        conn.close()
    num = listretotal//30
    res = requests.get(baseurl.format(key,int(page)-num),headers=headers)
    text = res.text.encode('utf-8').decode('unicode_escape')
    text = text.replace('jQuery191017984181955718603_1543829841888(','').replace(');','').replace(' rel="information">Detail<\/aute-htr_005"','').replace('<a href="\/cdn-cgi\/l\/email-protection" class="__cf_email__" data-cfemail="a7f4eef4979796e7">[email&#160;protected]<\/a>', '')
    dictext = eval(text)
    total = dictext['total']
    if total == 0 and listretotal == 0:
        return (0,1)
    elif len(listre) == 31:
        dic = listre[1:]
        return (dic,int(total)+listretotal)
    else:
        if len(listre) > 1:
                dic = listre[1:]
        if total != 0:
            total = int(total) + listretotal
            datas = dictext['data']
            for btid in datas:
                title = datas[btid]['title']
                size = datas[btid]['size']
                day = datas[btid]['day']
                hits = datas[btid]['hits']
                dic.append((btid,title,size,day,hits,''))
        else:
            total = len(dic)
        return (dic,total)
