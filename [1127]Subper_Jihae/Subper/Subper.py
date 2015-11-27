import sqlite3
import re

from flask import Flask, request, session, g, url_for, redirect, \
    render_template, abort, flash


#configuration
DATABASE = 'test.db'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)    #app.config는 플라스크 설정과 관련된 딕셔너리 객체
                                    #from_object함수는 대문자로 설정된 값들을 config에 추가

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.before_request
def before_request():
    g.db = connect_db() #g:flask의 전역 클래스 인스턴스


@app.route('/search', methods = ['GET', 'POST'])
def search():
    return render_template('search.html')


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


@app.route('/info/<pname>')
def performer_info(pname):
    cur = g.db.execute('select f.pname, f.fpage, f.fprof, f.fpic, f.fcover, d.dprof from finfo f, dinfo d where f.pname='+"'"+pname+"'"+' and f.pname=d.pname')

    for row in cur.fetchall():
        result = dict(pname=row[0], fpage=row[1], fprof=row[2], fpic=row[3], fcover=row[4], dprof=row[5])


    return render_template('performer_info.html', result = result)



if __name__ == '__main__':
    app.debug = True        #개발할 때만 이렇게
    app.run(host='127.0.0.1', port=5000)

