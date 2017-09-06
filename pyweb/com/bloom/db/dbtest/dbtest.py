# coding=utf8
'''
Created on 2017年9月4日

@author: Administrator
'''
import datetime

import DateCheckUtil as dateUtil
import MysqlManage as Mysql
import bizutil.DBNewsUtil as newsUtil


# import DbManager as DbManager
# import DbManager.DB as mysql
mysql = Mysql.Mysql()

def test_ping():
    size = mysql.getOne("select count(1) from pa_voice_newslog")
    print size
def test_mysql():
    mysql = Mysql.Mysql()
    
    now_time  = datetime.datetime.now()
    timeStr   = datetime.datetime.strftime(now_time,'%Y-%m-%d')
    timeDate  = datetime.datetime.strptime(timeStr,'%Y-%m-%d')
    
    
    
    sql = "insert into pa_voice_newslog (newslog_task,newslog_date,newslog_count) values( %(newslog_task)s,%(newslog_date)s,%(newslog_count)s )"
    param={'newslog_task':525,'newslog_date':timeDate,'newslog_count':1}
    
    
    mysql.insertOne(sql, param)
    
    size = mysql.getOne("select count(1) from pa_voice_newslog")
    print size
def test_newsUtil():
    db = newsUtil.DBNews()
#     print db.getNextVal()
#     url = 'http://finance.sina.com.cn/stock/stocktalk/2017-09-04/doc-ifykpuui0965047.shtml'
#     url = 'http://finance.sina.com.cn/roll/2017-09-05/doc-ifykpuui1008866.shtml'
#     url = 'http://dem03.com1'
#     param={"news_url":url}
#     isexist = db.isExistNewsMsg(param)
#     print isexist
    taskNum = db.getNextVal()
    news_date = dateUtil.currDateFormate()
    url = 'exampleeeeee'
    rMsg = '~~~~~~~~~~~'
    param={'news_task':taskNum,
           'news_date':news_date,
           'news_url':url,
           'news_message':rMsg}
    
    db.saveNews(param)
    print 'end'
def test_new():
    db = newsUtil.DBNews()
    taskNum = db.getNextVal()
    currDate = dateUtil.currDateFormateA()
    comment = 'AAA'
    succLen = 20 
    length = 25
    if succLen ==0 :
        comment = '短时间内重复访问，地址重复！'
    if succLen < length :
        comment = str(succLen)+'/'+str(length)+',存在部分请求信息获取失败'
    else:
        comment = 'SUCCESS'
    print comment
    param={'newslog_task':taskNum,'newslog_date':currDate,'newslog_count':length,'newslog_comment':comment}
    db.saveNewslog(param);  
    print 'END'
    
# test_newsUtil()
test_ping()

