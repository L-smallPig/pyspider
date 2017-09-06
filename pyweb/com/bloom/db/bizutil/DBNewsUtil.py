# coding=utf8
'''
Created on 2017年9月4日

@author: Administrator
'''
import MysqlManage as MysqlManage


class DBNews(object): 
    __db = None
    def __init__(self): 
        self.__db = MysqlManage.Mysql()  # MysqlManage.Mysql()self.getDB()
        
    def getDB(self):
        return self.__db  # MysqlManage.Mysql()
    def getNextVal(self):
        param = {}
        count = self.__db.getOne("SELECT Auto_increment + 1 FROM information_schema.`TABLES` WHERE Table_Schema='paface' AND table_name = 'pa_voice_newslog'", param);
        return count[0]
    def saveNewslog(self, param):
#         param={}
#         timeDate = dateUtil.currDateFormateA()
        sql = "insert into pa_voice_newslog (newslog_task,newslog_date,newslog_count,newslog_comment) values( %(newslog_task)s,%(newslog_date)s,%(newslog_count)s,%(newslog_comment)s )"
    #     param={'newslog_task':getNextVal(),'newslog_date':timeDate,'newslog_count':1}
        self.__db.insertOne(sql, param)
    def saveNews(self, param):
        sql = "insert into pa_voice_news (news_task,news_date,news_url,news_message,news_scope) values( %(news_task)s,%(news_date)s,%(news_url)s,%(news_message)s,%(news_scope)s )"
        self.__db.insertOne(sql, param)        
    def isExistNewsMsg(self, param):
        sql = "select count(1) from pa_voice_news where news_url = %(news_url)s"
        count = self.__db.getOne(sql, param)
        return count[0] > 0
        
