import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote, urljoin
import sqlite3 as sqlite
import webbrowser

#DB생성 및 테이블 생성
con= sqlite.connect("test.db")
cur=con.cursor()

##dropsql='''drop table if exists finfo;'''
##cur.execute(dropsql)

##sql='''create table finfo(
##num integer primary key autoincrement,
##pname string,
##fpage string,
##fprof string,
##fpic string,
##fcover string);'''
##cur.execute(sql)

##dropsql='''drop table if exists dinfo;'''
##cur.execute(dropsql)

##sql='''create table dinfo(
##num integer primary key autoincrement,
##pname string,
##dprof string);'''
##cur.execute(sql)


#페북에서 정보 가져오기
def crawlFacebook(input):
    url = "https://www.facebook.com/search/pages/?q="+quote(input)

    webbrowser.open(url)

    #1)해당 공연자의 페이지 주소 찾기
    with urlopen(url) as f:
        txt = str(f.read())

        pat = '(?<=<div class="_gll"><a href='+'"'+').+?(?='+'"'+'><div)'
        pattern = re.compile(pat)
        titles = pattern.findall(txt)

        pat2 = '(?<=<div class="_glm"><div class="_pac" data-bt="&#123;&quot;ct&quot;:&quot;sub_headers&quot;&#125;">).+?(?=</div>)'
        pattern2 = re.compile(pat2)
        cates = pattern2.findall(txt)


        #해당 페이지가 음악가/밴드 인지 체크
        temp_band = str(('음악가/밴드').encode("utf-8"))
        band = temp_band[2:-1]
        temp_yong = str(('비영리 단체').encode("utf-8"))
        yong = temp_yong[2:-1]
        temp_art = str(('예술가').encode("utf-8"))
        art = temp_art[2:-1]



        index = -1
        for i in range(len(cates)):
            if (cates[i] == band) | (cates[i] == yong) | (cates[i] == art):
                index = i

        if index == -1:
            return False


    #2)해당 공연자의 소개를 찾기
    url2 = titles[index]+"info/?tab=page_info"


    data = urlopen(url2)


    soup = BeautifulSoup(data, 'html.parser')
    pages = soup('div', {'class':"_4bl9"})


    profile = ""
    for page in pages:
        pwhole = page.contents
        for p in pwhole:
            data = p.contents
            for d in data:
                profile += (str(d)+"<br/>")


    #3)해당 공연자의 프로필 사진, 커버사진 페이지 주소 찾아오기
    with urlopen(titles[index]) as f:
        txt = str(f.read())

        pat = '(?<=<a class="profilePicThumb" href='+'"'+').+?(?='+'"'+' rel="theater">)'
        pattern = re.compile(pat)
        profileImg = pattern.findall(txt)

        pat2 = '(?<=<a class="_117p" href='+'"'+').+?(?='+'"'+' rel="theater")'
        pattern2 = re.compile(pat2)
        coverImg = pattern2.findall(txt)


    #4)해당 페이지의 프로필사진 src 찾아오기
    url3 = "https://www.facebook.com"+profileImg[0]

    data = urlopen(url3)

    soup = BeautifulSoup(data, 'html.parser')
    pages = soup('img', {'id':"fbPhotoImage"})

    #이게 이미지 소스!
    pimg = pages[0]['src']


    #5)해당 페이지의 커버사진 src 찾아오기
    url4 = "https://www.facebook.com"+coverImg[0]

    data = urlopen(url4)

    soup = BeautifulSoup(data, 'html.parser')
    pages = soup('img', {'id':"fbPhotoImage"})

    #이게 이미지 소스!
    cimg = pages[0]['src']


    #6)디비에 저장
    sql = 'insert into info (pname, fpage, fprof, fpic, fcover) values(?,?,?,?,?);'
    cur.execute(sql, (input, titles[index], profile, pimg, cimg))

    return True

#다음에서 정보 가져오기
def crawlDaum(num, inList):

    url = "http://cafe.daum.net/_c21_/bbs_read?grpid=1WHln&mgrpid=&fldid=ZYT1&datanum="+str(num)

    data = urlopen(url)
    print(data)

    soup = BeautifulSoup(data, 'html.parser')

    #이미지 소스
    pages = soup('img', {'class':"txc-image"})
    dimg = pages[1]['src']
    #print(dimg)


    #게시글 이름
    pages = soup('div', {'class':"subject"})
    title = pages[0].contents[3].contents[0].contents[0]


    for artist in inList:
        pattern = re.compile(artist)
        result = pattern.search(title)
        result = bool(result)
        if result:
            #6)디비에 저장
            sql = 'insert into dinfo (pname, dprof) values(?,?);'
            cur.execute(sql, (artist, str(dimg)))


#아티스트 리스트 만들기
artistList = []
selectsql = 'select distinct pname from performance'
cur.execute(selectsql)
for row in cur:
    artistList.append(row[0])


##1) FaceBook 정보 저장
#for artist in artistList:
#    print(artist, end=":")
#    result = crawlFacebook(artist)
#    print(result)

#con.commit()

##2) daum 정보 저장
#for i in range(29, 68):
#    crawlDaum(i, artistList)

#con.commit()


#디비에 들어갔나 확인
#sql = 'select * from dinfo'
#cur.execute(sql)

#f = open("test3.txt", "w", encoding="utf-8")
#for row in cur:
#    for r in row:
#        f.write(str(r))