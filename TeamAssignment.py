from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin
import re
import sqlite3 as sqlite

#DB생성 및 테이블 생성
con= sqlite.connect("test.db")

cur=con.cursor()
dropsql='''drop table if exists performance;'''
cur.execute(dropsql)

sql='''create table performance(
pnum integer primary key autoincrement,
pname string not null,
pgenre string not null,
pplace string not null,
psdate string not null,
pedate string not null);'''
cur.execute(sql)

#XML을 파싱하여 DB에 저장하는 함수
def parse(date):
    url='http://openapi.seoul.go.kr:8088/6f46496a4a6368653830617771776a/xml/MetroPerformanceInfo/1/900/'+date
    data=urlopen(url)
    soup = BeautifulSoup(data, "html.parser")

    #공연 갯수 파싱
    listnum = soup.find('list_total_count')
    countper = re.search("<list_total_count>(.*)</list_total_count>", repr(listnum))

    #메세지 설명값 받기
    code = soup.find('code')
    result = re.search("<code>(.*)</code>", repr(code))

    #INFO-000 정상처리이므로 파싱한 결과 출력
    if result.group(1) == "INFO-000":
        print(date+" 공연 갯수 : "+countper.group(1))
        #print("*****************"+date+" 공연정보*************************")
        #pnum -> 공연번호 파싱
        #print("-----공연 번호-----")
        pnum = soup.find_all('psche_seq')
        #print(psche_seq)
        for i in range(len(pnum)):
            str = repr(pnum[i])
            result = re.search("<psche_seq>(.*)</psche_seq>", str)
            pnum[i] = result.group(1)
            #print(pnum[i])

        #pname -> 공연자 or 공연팀 파싱
        #print("-----공연자-----")
        pname = soup.find_all('name')
        #print(pname)
        for i in range(len(pname)):
            str = repr(pname[i])
            result = re.search("<name>(.*)</name>", str)
            pname[i] = result.group(1)
            #print(pname[i])

        #pgenre -> 공연 내용(공연 장르) 파싱
        #print("-----공연 내용(장르)-----")
        pgenre = soup.find_all('cmt')
        #print(pgenre)
        for i in range(len(pgenre)):
            str = repr(pgenre[i])
            result = re.search("<cmt><!\W+CDATA\W+(.*)\W+\W+></cmt>", str)
            pgenre[i] = result.group(1)
            #print(pgenre[i])

        #pplace -> 공연 장소 파싱
        #print("-----공연 장소-----")
        pplace = soup.find_all('place')
        #print(pplace)
        for i in range(len(pplace)):
            str = repr(pplace[i])
            result = re.search("<place>(.*)</place>", str)
            pplace[i] = result.group(1)
            #print(pplace[i])

        #psdate -> 공연 시작시간 파싱
        #print("-----공연 시작시간-----")
        psdate = soup.find_all('sdate')
        #print(psdate)
        for i in range(len(psdate)):
            str = repr(psdate[i])
            result = re.search("<sdate>(.*)</sdate>", str)
            psdate[i] = result.group(1)
            #print(psdate[i])

        #pedate -> 공연 종료시간 파싱
        #print("-----공연 종료시간-----")
        pedate = soup.find_all('edate')
        #print(pedate)
        for i in range(len(pedate)):
            str = repr(pedate[i])
            result = re.search("<edate>(.*)</edate>", str)
            pedate[i] = result.group(1)
            #print(pedate[i])

        
        #data라는 투플안에 정보 모아서 insertsql할때 넣어줌
        for i in range(int(countper.group(1))):
            data=((pname[i],pgenre[i],pplace[i],psdate[i],pedate[i]))           
            insertsql='''insert into performance(pname,pgenre,pplace,psdate,pedate)
                         values(?,?,?,?,?);'''
            cur.execute(insertsql, data)
        
        con.commit()
       

    #INFO-200 정상처리는 되었으나 데이터가 없음
    elif result.group(1) == "INFO-200" :
        print("해당데이터가 없습니다.")
    #나머지는 모두 ERROR이므로 다시 입력해서 아무것도 실행하지 않고 입력값을 다시 받음
    else :
        print("다시 입력해주세요")

#각 필드별로 어떤 값이 있는지 보여주는 함수
def showField(input_field):
    print()
    
    #인풋으로 받은 필드 명을 넣어서 쿼리문으로 만듬
    selectsql = 'select distinct '+input_field+' from performance'
    cur.execute(selectsql)
    for row in cur:
        print(row[0], end = " // ")

    print("\n")

#str으로 검색했을 때 나오는 공연들 출력
def searchShow(input_field, input_str):
 
    #검색하고자 하는 필드와 검색어가 맞는 경우 출력한다.
    selectsql = 'select * from performance where '+input_field+'='+"'"+input_str+"'"
    cur.execute(selectsql)

    result = cur.fetchall()

    if len(result) == 0:
        print("\n검색 결과가 없습니다.")
    else:
        print()
        for item in result:
            print("%s %s %s %s %s" % (item[1], item[2], item[3], item[4], item[5]))

    print("\n")


#date_list에 원하는 날짜(년도-월)을 넣어두었다.
date_list=["2015-01","2015-02","2015-03","2015-04","2015-05","2015-06",
           "2015-07","2015-08","2015-09","2015-10","2015-11","2015-12"]

#각 달별로 parse
print("============파싱 중============")
for item in date_list:
    parse(item)
print("===========파싱 완료===========")

print("\n=====검색필드를 선택하세요=====")
print("1) 공연자명")
print("2) 공연장르")
print("3) 공연장소")

while(True):
    field = input("입력 (1~3) : ")

    if field == "1":
        field = "pname"
        break
    elif field == "2":
        field = "pgenre"
        break
    elif field == "3":
        field = "pplace"
        break
    else:
        print("\n1~3의 숫자를 입력해주세요")

showField(field)

str = input("위의 내용중 하나를 선택하세요 : ")
searchShow(field, str)