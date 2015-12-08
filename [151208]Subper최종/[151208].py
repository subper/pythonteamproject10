import sqlite3, re
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from contextlib import closing
import datetime, time
from random import shuffle

#configuration
DATABASE = 'test.db'
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)



def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.before_request
def before_request():
    g.db = connect_db() #g:flask의 전역 클래스 인스턴스

#회원가입
@app.route('/add', methods=['POST'])
def add_member():
    email = request.form['email']
    pwd = request.form['pwd']
    pwd_ck = request.form['pwd_ck']

    cur = g.db.execute('select email from member')
    members = [dict(email=row[0]) for row in cur.fetchall()]

    for mem in members:
        if mem['email'] == email:
            flash('이미 존재하는 이메일입니다.')
            return redirect(url_for('show_calender'))

    if pwd != pwd_ck:
        flash('비밀번호를 다시 확인해주세요.')
        return redirect(url_for('show_calender'))

    pattern1 = re.compile("[a-zA-Z]+")
    result1 = pattern1.search(pwd)

    pattern2 = re.compile("[0-9]+")
    result2 = pattern2.search(pwd)

    if result1 == None or result2 == None:
        flash('비밀번호는 문자와 숫자를 포함해야합니다.')
        return redirect(url_for('show_calender'))

    g.db.execute('insert into member (email, pwd) values (?, ?)', [request.form['email'], request.form['pwd']])
    g.db.commit()
    flash('회원가입이 완료되었습니다.')

    return redirect(url_for('show_calender'))

#로그인
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    pwd = request.form['pwd']

    cur = g.db.execute('select email, pwd from member')
    members = [dict(email=row[0], pwd=row[1]) for row in cur.fetchall()]

    print(email)
    print(pwd)
    for step in range(len(members)):
        print(members[step])

    for mem in members:
        if mem['email'] == email:
            if mem['pwd'] == pwd:
                session['logged_in'] = True 
                session['email']=email
                flash('로그인되었습니다. 환영합니다.')
                return redirect(url_for('show_calender'))

            flash('비밀번호가 잘못되었습니다.')
            return redirect(url_for('show_calender'))

    flash('존재하지 않는 이메일입니다.')
    return redirect(url_for('show_calender'))

#로그아웃
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('email', None)
    flash('로그아웃되었습니다.')
    return redirect(url_for('show_calender'))

#마이페이지
@app.route('/mypage')
def show_mypage():
    email=session['email']
    cur = g.db.execute('select distinct f.fpic, p.pname, p.pgenre, p.pplace, p.psdate, p.pedate, p.pnum from performance p, finfo f, like l where l.email="'+email+'" and l.pnum=p.pnum and f.pname=p.pname')
    result = [dict(pic=row[0], name=row[1], genre=row[2], place=row[3], time=row[4]+" ~ "+row[5], num=row[6]) for row in cur.fetchall()]

    recom = [0, 0, 0, 0, 0, 0]

    for row in result: 
        print(row['genre'])
        if (row['genre'] == '인디밴드') or (row['genre'] =='인디(보컬솔로)'):
            recom[0] += 1
        elif (row['genre'] == '통기타라이브') or (row['genre'] =='라틴팝/안데스음악') or (row['genre'] =='재즈밴드'):
            recom[1] += 1
        elif (row['genre'] == '힙합') or (row['genre'] =='K-POP'):
            recom[2] += 1
        elif (row['genre'] == '7080') or(row['genre'] == '댄스퍼포먼스(택견)') or (row['genre'] =='MC레크레이션') \
            or (row['genre'] =='MC,레크레이션') or (row['genre'] =='댄스퍼포먼스(태껸)') or (row['genre'] =='태껸'):
            recom[3] += 1
        elif (row['genre'] == '아카펠라') or (row['genre'] =='합창'):
            recom[4] += 1
        elif (row['genre'] == '피아노연주') or (row['genre'] =='오카리나연주') or (row['genre'] =='색소폰앙상블') or (row['genre'] =='색소폰연주') \
            or (row['genre'] =='우쿠렐레연주') or (row['genre'] =='피아노 7중주'):
            recom[5] += 1
        elif (row['genre'] == '클래식(팬플룻/팝페라)') or (row['genre'] =='클래식(비올라)') or (row['genre'] =='클래식(현악5중주)') \
            or (row['genre'] =='클래식(팝페라)') or (row['genre'] =='클래식(금관앙상블)') or (row['genre'] =='클래식(트롬본앙상블)') \
            or (row['genre'] =='클래식(팬플릇팝페라)') or (row['genre'] =='클래식(피아노7중주)'):
            recom[6] += 1
    
    top = 0
    index = 0
    for i in range(0,6):
        if top < recom[i]:
            index = i
            top = recom[i]


    today = "2015-10-01 00:00"

    if index == 0:
        cur = g.db.execute("select f.fpic, p.pname, p.pgenre, p.pplace, p.psdate, p.pedate, p.pnum from performance p, finfo f where f.pname=p.pname and p.psdate > "+"'"+today+"'"+" and (p.pgenre like '%인디%') order by random() limit 5;")
        result2 = [dict(pic=row[0], name=row[1], genre=row[2], place=row[3], time=row[4]+" ~ "+row[5], num=row[6]) for row in cur.fetchall()]
    elif index == 1:
        cur = g.db.execute("select f.fpic, p.pname, p.pgenre, p.pplace, p.psdate, p.pedate, p.pnum from performance p, finfo f where f.pname=p.pname and p.psdate > "+"'"+today+"'"+" and (p.pgenre like '%통기타%' or pgenre like '%라틴%' or pgenre like '%재즈%') order by random() limit 5;")
        result2 = [dict(pic=row[0], name=row[1], genre=row[2], place=row[3], time=row[4]+" ~ "+row[5], num=row[6]) for row in cur.fetchall()]
    elif index == 2:
        cur = g.db.execute("select f.fpic, p.pname, p.pgenre, p.pplace, p.psdate, p.pedate, p.pnum from performance p, finfo f where f.pname=p.pname and p.psdate > "+"'"+today+"'"+" and (p.pgenre like '%힙합%' or pgenre like '%K-POP%') order by random() limit 5;")
        result2 = [dict(pic=row[0], name=row[1], genre=row[2], place=row[3], time=row[4]+" ~ "+row[5], num=row[6]) for row in cur.fetchall()]
    elif index == 3:
        cur = g.db.execute("select f.fpic, p.pname, p.pgenre, p.pplace, p.psdate, p.pedate, p.pnum from performance p, finfo f where f.pname=p.pname and p.psdate > "+"'"+today+"'"+" and (p.pgenre like '%7080%' or pgenre like '%택견%' or pgenre like '%태껸%' or pgenre like '%MC%') order by random() limit 5;")
        result2 = [dict(pic=row[0], name=row[1], genre=row[2], place=row[3], time=row[4]+" ~ "+row[5], num=row[6]) for row in cur.fetchall()]
    elif index == 4:
        cur = g.db.execute("select f.fpic, p.pname, p.pgenre, p.pplace, p.psdate, p.pedate, p.pnum from performance p, finfo f where f.pname=p.pname and p.psdate > "+"'"+today+"'"+" and (p.pgenre like '%아카펠라%' or pgenre like '%합창%') order by random() limit 5;")
        result2 = [dict(pic=row[0], name=row[1], genre=row[2], place=row[3], time=row[4]+" ~ "+row[5], num=row[6]) for row in cur.fetchall()]
    elif index == 5:
        cur = g.db.execute("select f.fpic, p.pname, p.pgenre, p.pplace, p.psdate, p.pedate, p.pnum from performance p, finfo f where f.pname=p.pname and p.psdate > "+"'"+today+"'"+" and (p.pgenre like '%연주%' or pgenre like '%색소폰%' or pgenre like '%피아노%') order by random() limit 5;")
        result2 = [dict(pic=row[0], name=row[1], genre=row[2], place=row[3], time=row[4]+" ~ "+row[5], num=row[6]) for row in cur.fetchall()]
    elif index == 6:
        cur = g.db.execute("select f.fpic, p.pname, p.pgenre, p.pplace, p.psdate, p.pedate, p.pnum from performance p, finfo f where f.pname=p.pname and p.psdate > "+"'"+today+"'"+" and (p.pgenre like '%클래식%') order by random() limit 5;")
        result2 = [dict(pic=row[0], name=row[1], genre=row[2], place=row[3], time=row[4]+" ~ "+row[5], num=row[6]) for row in cur.fetchall()]
 
    return render_template('mypage.html', result = result, result2 = result2)

#홈
@app.route('/')
def index():

    result = []

    cur = g.db.execute('select distinct fcover,pname from finfo')

    for row in cur.fetchall():
        if row[0] != None:
            result.append(dict(fcover=row[0], pname=row[1]))

    shuffle(result)

    return render_template('index.html', result=result)

#검색하기
@app.route('/search', methods = ['GET', 'POST'])
def search():
    return render_template('search.html')

#검색결과
@app.route('/search/result', methods = ['GET', 'POST'])
def search_result():
    input = request.form['input']
    category = request.form['category']

    today = "2015-08-01 00:00"
    #today = time.strftime("%Y-%m-%d %I:%M", time.localtime())

    if category == "name":
        cur = g.db.execute('select distinct f.fpic,p.pname,p.pgenre,p.pplace,p.psdate,p.pedate,p.pnum from performance p, finfo f where p.pname like '+"'%"+input+"%'"+' and p.psdate > '+"'"+today+"'"+'  and f.pname=p.pname')
        result = [dict(pic=row[0], name=row[1], genre=row[2], place=row[3], time=row[4]+" ~ "+row[5], num=row[6]) for row in cur.fetchall()]
    elif category == "genre":
        cur = g.db.execute('select distinct f.fpic,p.pname,p.pgenre,p.pplace,p.psdate,p.pedate,p.pnum from performance p, finfo f where p.pgenre like '+"'%"+input+"%'"+' and p.psdate > '+"'"+today+"'"+'  and f.pname=p.pname')
        result = [dict(pic=row[0], name=row[1], genre=row[2], place=row[3], time=row[4]+" ~ "+row[5], num=row[6]) for row in cur.fetchall()]
    else:
        pass

    likepnum = []

    if session.get('logged_in'):
        cur = g.db.execute('select pnum from like where email='+"'"+session['email']+"';")

        for row in cur.fetchall():
            likepnum.append(row[0])     


    return render_template('search_result.html', result = result, likepnum=likepnum)

#공연자 정보
@app.route('/info/<pname>')
def performer_info(pname):
    tag = re.compile("<.+?>")

    cur = g.db.execute('select f.pname, f.fpage, f.fprof, f.fpic, f.fcover, d.dprof from finfo f, dinfo d where f.pname='+"'"+pname+"'"+' and f.pname=d.pname')


    for row in cur.fetchall():
        if row[2] == None:
            result = dict(pname=row[0], fpage=row[1], fprof=tag.split("nostring"), fpic=row[3], fcover=row[4], dprof=row[5])
        else:
            result = dict(pname=row[0], fpage=row[1], fprof=tag.split(row[2]), fpic=row[3], fcover=row[4], dprof=row[5])

    return render_template('performer_info.html', result = result)

#공연캘린더
@app.route('/calender')
def show_calender():
    return render_template('calender.html')

#공연캘린더 결과
@app.route('/calender/result', methods = ['GET', 'POST'])
def calender_result():
    pdate = request.form['pdate']
   
    cur = g.db.execute('select distinct f.fpic, p.pname, p.pgenre, p.pplace, p.psdate, p.pedate,p.pnum  from performance p, finfo f where p.psdate like '+"'%"+pdate+"%'"+' and f.pname=p.pname')
    result = [dict(pic=row[0], name=row[1], genre=row[2], place=row[3], time=row[4]+" ~ "+row[5], num=row[6]) for row in cur.fetchall()]
    

    likepnum = []

    if session.get('logged_in'):
        cur = g.db.execute('select pnum from like where email='+"'"+session['email']+"';")

        for row in cur.fetchall():
            likepnum.append(row[0])      

    return render_template('calender_result.html', result = result, likepnum=likepnum)

#공연노선도
@app.route('/linemap',methods = ['GET', 'POST'])
def linemap():
    return render_template('linemap.html')

#공연노선도 결과
@app.route('/linemap/result', methods = ['GET', 'POST'])
def linemap_result():
    place = request.form['place']
    today = "2015-10-01 00:00"
    cur = g.db.execute('select distinct f.fpic,p.pname,p.pgenre,p.pplace,p.psdate,p.pedate,p.pnum from performance p, finfo f where p.pplace like '+"'%"+place+"%'"+' and p.psdate > '+"'"+today+"'"+'  and f.pname=p.pname')
    result = [dict(pic=row[0], name=row[1], genre=row[2], place=row[3], time=row[4]+" ~ "+row[5], num=row[6]) for row in cur.fetchall()]

    likepnum = []

    if session.get('logged_in'):
        cur = g.db.execute('select pnum from like where email='+"'"+session['email']+"';")

        for row in cur.fetchall():
            likepnum.append(row[0])

    return render_template('map_result.html', result = result, likepnum=likepnum)

#공연좋아요 기능
@app.route('/like/<pnum>',methods = ['GET', 'POST'])
def like(pnum):
    email=session['email']
    g.db.execute('insert into like (pnum, email) values (?, ?)', [pnum, session['email']])
    g.db.commit()

    return redirect(url_for('show_mypage'))

#공연좋아요삭제 기능
@app.route('/nolike/<pnum>',methods = ['GET', 'POST'])
def nolike(pnum):
    email=session['email']
    g.db.execute('delete from like where pnum="'+pnum+'" and email="'+email+'"')
    g.db.commit()

    return redirect(url_for('show_mypage'))

if __name__ == '__main__':
    app.debug=True
    app.run(host="192.168.10.2", port=5000)
    #app.run(host="127.0.0.1", port=5000)

