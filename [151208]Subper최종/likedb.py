from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin
import re
import sqlite3 as sqlite

con= sqlite.connect("test.db")
cur=con.cursor()

#cur.execute("select * from like;") 
#for row in cur: 
#    print(row) 
#    print(row[0])
#pnum=1
#email="aaa@naver.com"
#insert = cur.execute('insert into like (pnum, email) values (?, ?)', [pnum,email])

#cur.execute("select pgenre from performance;") 
#for row in cur: 
#    #print(row) 
#    print(row[0])

recom = [0, 0, 0, 0, 0, 0, 0]

#for row in cur: 
#    print(row[0])
#    if (row[0] == "인디밴드") or (row[0] =="인디(보컬솔로)"):
#        recom[0] = recom[0] + 1
#    elif (row[0] == "통기타라이브") or (row[0] =="라틴팝/안데스음악") or (row[0] =="재즈밴드"):
#        recom[1] = recom[1] + 1
#    elif (row[0] == "힙합") or (row[0] =="K-POP"):
#        recom[2] = recom[2] + 1
#    elif (row[0] == "7080") or(row[0] == "댄스퍼포먼스(택견)") or (row[0] =="MC레크레이션") \
#        or (row[0] =="MC,레크레이션") or (row[0] =="댄스퍼포먼스(태껸)") or (row[0] =="태껸"):
#        recom[3] = recom[3] + 1
#    elif (row[0] == "아카펠라") or (row[0] =="합창"):
#        recom[4] = recom[4] + 1
#    elif (row[0] == "피아노연주") or (row[0] =="오카리나연주") or (row[0] =="색소폰앙상블") or (row[0] =="색소폰연주") \
#        or (row[0] =="우쿠렐레연주") or (row[0] =="피아노 7중주"):
#        recom[5] = recom[5] + 1
#    elif (row[0] == "클래식(팬플룻/팝페라)") or (row[0] =="클래식(비올라)") or (row[0] =="클래식(현악5중주)") \
#        or (row[0] =="클래식(팝페라)") or (row[0] =="클래식(금관앙상블)") or (row[0] =="클래식(트롬본앙상블)") \
#        or (row[0] =="클래식(팬플릇팝페라)") or (row[0] =="클래식(피아노7중주)"):
#        recom[6] = recom[6] + 1


top = 0
index = 0
for i in range(0,6):
    if top < recom[i]:
        index = i
        top = recom[i]

print(index, top)        
print(recom)

if index == '0':
    cur.execute("select pname, pgenre from performance where pgenre like '%인디%' order by random();")
elif index == '1':
    cur.execute("select pname, pgenre from performance where pgenre like '%통기타%' or pgenre like '%라틴%' or pgenre like '%재즈%' order by random();")
elif index == '2':
    cur.execute("select pname, pgenre from performance where pgenre like '%힙합%' or pgenre like '%K-POP%' order by random();")
elif index == '3':
    cur.execute("select pname, pgenre from performance where pgenre like '%7080%' or pgenre like '%택견%' or pgenre like '%태껸%' or pgenre like '%MC%' order by random();")
elif index == '4':
    cur.execute("select pname, pgenre from performance where pgenre like '%아카펠라%' or pgenre like '%합창%' order by random();")
elif index == '5':
    cur.execute("select pname, pgenre from performance where pgenre like '%연주%' or pgenre like '%색소폰%' or pgenre like '%피아노%' order by random();")
elif index == '6':
    cur.execute("select pname, pgenre from performance where pgenre like '%클래식%' order by random();")

for row in cur: 
    print(row) 
#    print(row[0])



#email = 'ddangkong'
#cur.execute('select distinct f.fpic, p.pname, p.pgenre, p.pplace, p.psdate, p.pedate from performance p, finfo f, like l where l.email like '+"'%"+email+"%' and l.pnum=p.pnum and f.pname=p.pname")
#for row in cur: 
#    print(row) 
#    print(row[0])


#con.commit()
con.close()