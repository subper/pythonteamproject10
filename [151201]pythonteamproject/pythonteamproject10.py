import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from contextlib import closing

#configuration
DATABASE = 'test.db'
DEBUG = True

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

#검색하기
@app.route('/search', methods = ['GET', 'POST'])
def search():
    return render_template('search.html')

#검색결과
@app.route('/search/result', methods = ['GET', 'POST'])
def search_result():
    input = request.form['input']
    category = request.form['category']

    if category == "name":
        cur = g.db.execute('select f.fpic,p.pname,p.pgenre,p.pplace,p.psdate,p.pedate from performance p, finfo f where p.pname like '+"'%"+input+"%'"+' and f.pname=p.pname')
        result = [dict(pic=row[0], name=row[1], genre=row[2], place=row[3], time=row[4]+" ~ "+row[5]) for row in cur.fetchall()]

    elif category == "genre":
        cur = g.db.execute('select f.fpic,p.pname,p.pgenre,p.pplace,p.psdate,p.pedate from performance p, finfo f where p.pgenre like '+"'%"+input+"%'"+' and f.pname=p.pname')
        result = [dict(pic=row[0], name=row[1], genre=row[2], place=row[3], time=row[4]+" ~ "+row[5]) for row in cur.fetchall()]
    else:
        pass

    return render_template('search_result.html', result = result)

#공연자 정보
@app.route('/info/<pname>')
def performer_info(pname):
    cur = g.db.execute('select f.pname, f.fpage, f.fprof, f.fpic, f.fcover, d.dprof from finfo f, dinfo d where f.pname='+"'"+pname+"'"+' and f.pname=d.pname')

    for row in cur.fetchall():
        result = dict(pname=row[0], fpage=row[1], fprof=row[2], fpic=row[3], fcover=row[4], dprof=row[5])

    return render_template('performer_info.html', result = result)

#공연캘린더
@app.route('/calender')
def show_calender():
    return render_template('calender.html')

#공연캘린더 결과
@app.route('/calender/result', methods = ['GET', 'POST'])
def calender_result():
    pdate = request.form['pdate']
    cur = g.db.execute('select f.fpic, p.pname, p.pgenre, p.pplace, p.psdate, p.pedate from performance p, finfo f where p.psdate like '+"'%"+pdate+"%'"+' and f.pname=p.pname')
    result = [dict(pic=row[0], name=row[1], genre=row[2], place=row[3], time=row[4]+" ~ "+row[5]) for row in cur.fetchall()]

    return render_template('calender_result.html', result = result)

if __name__ == '__main__':
    app.debug=True
    app.run(host="127.0.0.1")
