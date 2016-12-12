#-*-coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup as bs
import time as ti
import random
import string
import MySQLdb as mdb



headers={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Host':'pm25.in',
'Referer':'http://pm25.in/',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'

}



def insertdata(sql):
    db = mdb.connect(" ","",'','' )
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 设置编码UTF8
    cursor.execute('SET NAMES UTF8')
    try:
       # 执行sql语句
       cursor.execute(sql)
       # 提交到数据库执行
       db.commit()
    except:
       # 发生错误时回滚
       db.rollback()
       print sql
       print 'excute this sql error...'
       return 0
    # 关闭数据库连接
    db.close()


def selectdata(i):
    db = mdb.connect(" ","",'','' )
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 设置编码UTF8
    cursor.execute('SET NAMES UTF8')
    sql="SELECT location FROM `localation` WHERE ID=%d" %(i)
    try:
       # 执行sql语句
       cursor.execute(sql)
       # 提交到数据库执行
       db.commit()
       results = cursor.fetchall()
       if (results):
            for row in results:
              res = row[0] #找到某一个结果返回
            return res
    except:
       # 发生错误时回滚
       db.rollback()
       print sql
       print 'excute this sql error...'
       return 0
    # 关闭数据库连接
    db.close()

#定义函数获取信息，提取信息，并保存到数据库中
def getweatherinfo(city):
    url0="http://pm25.in"  #主页
    url1=url0+city
   #  print url1
    req=requests.get(url1).text
    #print req
    soup=bs(req,"html.parser")
    time0=soup.find("div",class_="live_data_time") #提取时间
   # time1=time0.get_text()
    p=re.compile("\d+.*\d+")
    p1=re.compile("\s")
    time1=re.search(p,str(time0)).group().strip().encode("utf-8")
    #print time1
    city0=soup.find("div",class_="city_name")#提取地点
    city=city0.get_text().strip().encode("utf-8")
    #print city
    level0=soup.find("div",class_="level") #提取污染水平
    level=level0.get_text().strip().encode("utf-8")
    #print level


    value=soup.find_all("div",class_="value")
    baqi=value[0].get_text().strip().encode("utf-8")
    #print baqi
    bqm25=value[1].get_text().strip().encode("utf-8")
    #print bqm25
    bpm10=value[2].get_text().strip().encode("utf-8")
    # print bpm10
    bco=value[3].get_text().strip().encode("utf-8")
    # print bco
    bno2=value[4].get_text().strip().encode("utf-8")
    # print bno2
    bo31=value[5].get_text().strip().encode("utf-8")
    # print bo31
    bo38=value[6].get_text().strip().encode("utf-8")
   # print bo38
    bso2=value[7].get_text().strip().encode("utf-8")
    # print bso2







    #污染物，影响和建议
    pp0=soup.find("div",class_="primary_pollutant")
    pp1=pp0.get_text().strip()
    pp1=p1.sub("",pp1).encode("utf-8")
    #print pp1
    #  p1=re.compile("(：).+")#提取污染物，后面有:号
    # pp1=re.search(p1,str(pp1)).group()
    # print pp1
    # pp=pp1.lstrip('(：)')
    # print pp
    affect0=soup.find("div",class_="affect")
    # print affect0
    # affect1=re.search(p1,str(affect0)).group()
    # affect=affect1.lstrip("：")
    affect=affect0.get_text().strip()#提取影响
    affect=p1.sub("",affect).encode("utf-8")
    action0=soup.find("div",class_="action")
    # action1=re.search(p1,str(action0))
    # action=action.lstrip("：")
    action=action0.get_text().strip()#提取建议
    action=p1.sub("",action).encode("utf-8")
    sql="INSERT INTO `baseinfo`(`time`,`location`,`quality`,`AQI`,`PM25`,`PM10`,`CO`,`NO2`,`O31`,`O38`,`SO2`,`primaryp`,`influence`,`advice`) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(time1,city,level,baqi,bqm25,bpm10,bco,bno2,bo31,bo38,bso2,pp1,affect,action)
    insertdata(sql)




    #以下是详细信息
    tbody=soup.find("tbody")
    #print type(tbody)
    #soup1=bs(tbody,"html.parser")
    #print soup1
    tbo=str(tbody)
    tr=bs(tbo,"html.parser").find_all("tr")
    #   print len(tr)

    for i in range(len(tr)):
        location=tr[i]
        td=location.find_all("td")
        locations=td[0].get_text().encode("utf-8")
        aqi= td[1].get_text().encode("utf-8")
        qua=td[2].get_text().encode("utf-8")
        primaryp=td[3].get_text().encode("utf-8")
        pm25=td[4].get_text().encode("utf-8")
        pm10=td[5].get_text().encode("utf-8")
        co=td[6].get_text().encode("utf-8")
        no2=td[7].get_text().encode("utf-8")
        o31=td[8].get_text().encode("utf-8")
        o38=td[9].get_text().encode("utf-8")
        so2=td[10].get_text().encode("utf-8")
        # print locations
        # print aqi
        # print qua
        # print type(tbody)
        #   print tr[i].get_text()
        #   sql="INSERT INTO `dynamic`( `userid`, `dongtai`) VALUES (%d,'%s')" %(id,dongtai)
        #  操作，插入数据库中
        sql1="INSERT INTO `particularinfo`(`time`,`location`,`AQI`,`quality`,`primaryp`,`PM25`,`PM10`,`CO`,`NO2`,`O31`,`O38`,`SO2`)VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(time1,locations,aqi,qua,primaryp,pm25,pm10,co,no2,o31,o38,so2)
        insertdata(sql1)




#num=raw_input("输入多少天：")
#city=raw_input("输入城市(汉语拼音):")

for i in range(100000):
    #遍历城市：
    for m in range(69):
        city=selectdata(m+1)
        getweatherinfo(city)
        ti.sleep(6)
    ti.sleep(3000-72*6)

    #间隔半小时时间刷新数据
