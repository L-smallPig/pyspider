# coding=utf8
'''
Created on 2017年9月5日

@author: Administrator
'''
import os
import threading
import time
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

import com.bloom.sina.sina as sinanews


threadLock = threading.Lock()

class thread_sina_news(threading.Thread):
    def __init__(self, threadID,name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print 'starting ' +self.name
        threadLock.acquire()
        handle_sina_new()
        threadLock.release()

def biz_sina_new():
    thread_news = thread_sina_news(1,"thread_news")
    thread_news.start()
def handle_sina_new():
    print 'looking for news'
    print datetime.datetime.now()
    sinanews.telnet_news_sina()

if __name__=='__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(biz_sina_new,'cron',hour='*',minute='*/20',second='0',year='2017',day_of_week='mon-fri')
    
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    
    try:
        scheduler.start()
        while True:
            time.sleep(100)
#             print('waiting!')
    except(KeyboardInterrupt,SystemExit):
        scheduler.shutdown()
        print 'Exit !'
        
    