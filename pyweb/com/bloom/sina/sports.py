# coding=utf8
'''
Created on 2017年9月7日

@author: Administrator
'''

import re
import urllib2

from bs4 import BeautifulSoup
import requests

import DateCheckUtil as dateUtil
import bizutil.DBNewsUtil as DBNewsUtil


class sinaSport(object):
    def sina_encode_soup(self,url):
        res = requests.get(url)
        res.encoding = 'UTF-8'
        
        # 使用剖析器为html.parser
        soup = BeautifulSoup(res.text, 'html5lib')
        return soup
    def sport_soup(self,url):
#     url = 'http://roll.finance.sina.com.cn/s/channel.php?ch=03#col=45&spec=&type=&ch=03&k=&offset_page=0&offset_num=0&num=60&asc=&page=1'
#     url = 'http://roll.finance.sina.com.cn/s/channel.php?ch=03#col=49&spec=&type=&ch=03&k=&offset_page=0&offset_num=0&num=60&asc=&page=1'
        response = urllib2.urlopen(url)
        data = response.read()
        
        soup = BeautifulSoup(data, 'html5lib')
    
        return soup
    def sport_geturl_roll(self):
        #基础页面 未添加下标
        baseUrl = 'http://sports.sina.com.cn/'
        #index 默认获取前十页数据
        urlList = []

        soup = self.sina_encode_soup(baseUrl)
            
#             other sports
        othersport = soup.select('.ppcs_l.fl') 
        
        if len(othersport) > 0 :
            
            for index in range(0,len(othersport)-2):
                alist = othersport[index].select('.list01 a')
    #             print len(alist)
                for a2 in alist :
    #                 print a2.text,a2.get("href")
#                     print a2.text,a2.get("href")
                    urlList.append(a2.get("href"))
    #                 print a2.get('href')
    #                 print a2.text.decode('utf-8').incode('mbcs'),':',a2.get('href')
            
            
        else :
            print '未定位到[综合体育]'
        return urlList

    def sport_geturl_all(self):
#     urlList = finance_geturl_main_topMsg()
        urlList = self.sport_geturl_roll()
        print '页面捕获完毕，共计收集到地址：FINAL:',len(urlList)
        
        p_china  = r'http://sports.sina.com.cn/china/.*'
        p_basketball  = r'http://sports.sina.com.cn/basketball/.*'
        p_cba   = r'http://sports.sina.com.cn/cba/.*'
        p_g = r'http://sports.sina.com.cn/g/.*'
        
        rdicts = {}
        print '=============开始匹配==============='
        
        for url in urlList :
    #         print ii
            if url is not None :
                
                if rdicts.has_key(url):
                    #重复url，不再请求
                    continue
                if re.match(p_china, url, re.M) is not None or \
                   re.match(p_basketball, url, re.M) is not None or \
                   re.match(p_cba, url, re.M) is not None or \
                   re.match(p_g, url, re.M) is not None :
                    vmsg = self.sport_parse_china(url)
                else:
                    print '暂未匹配该路径',url
                    continue
                
                if vmsg is not None :
                    rdicts[url] = vmsg
            else :
                print 'URL为None 跳过'
        print '结果集如下',len(rdicts)
        for k,v in rdicts.items():
            print k
          
        return rdicts
    def sport_parse_china(self,url):
#         url = 'http://sports.sina.com.cn/china/j/2017-09-07/doc-ifykusey4365367.shtml'
#         url = 'http://sports.sina.com.cn/china/j/2017-09-07/doc-ifykqmrw1972290.shtml'
#         url = 'http://sports.sina.com.cn/china/national/2017-09-07/doc-ifykuffc4033461.shtml'
#         url = 'http://sports.sina.com.cn/basketball/nba/2017-09-07/doc-ifykuffc4036595.shtml'
#         url = 'http://sports.sina.com.cn/cba/2017-09-07/doc-ifykuffc4073454.shtml'
#         url = 'http://sports.sina.com.cn/g/pl/2017-09-07/doc-ifykuffc4062709.shtml'
        soup = self.sina_encode_soup(url)
        body = soup.select('#artibody')
        rarr = []
        if len(body)>0:
            pmsg = body[0].select('p')
            for msg in pmsg:
                rarr.append(msg.text)
#                 print msg.text 
        else :
            print 'find artibody failed',url
            return None
        rmsg = ''.join(rarr)   
#         print rmsg
        return rmsg
    def telnet_sport_main(self):
        mydb = DBNewsUtil.DBNews()
        
        rdicts = self.sport_geturl_all()
        length = len(rdicts)
        if length < 5 :
            print '结果集太少',str(length)
            return
        existLen= 0
        if(length > 0) :
            print '成功捕获访问地址个数：', length
            taskNum = mydb.getNextVal()
            for rUrl,rMsg in rdicts.items():
                print rUrl
                param={"news_url":rUrl}
                isexist = mydb.isExistNewsMsg(param)
                if isexist:
                    existLen+=1
                else:
                    news_date = dateUtil.currDateFormateA()
                    param={'news_task':taskNum,
                               'news_date':news_date,
                               'news_url':rUrl,
                               'news_message':rMsg,
                               'news_scope':'sports'}
                    mydb.saveNews(param)
                    
            currDate = dateUtil.currDateFormate()
            comment = ''
            if existLen>0:
                comment = '存在'+str(existLen)+'/'+str(length)+',短时间内重复请求.' 
            else:
                comment = 'SUCCESS'
            param={'newslog_task':taskNum,'newslog_date':currDate,'newslog_count':length,'newslog_comment':comment}
            mydb.saveNewslog(param); 
        print '成功处理完毕！'
if __name__ == "__main__":
    
    sports = sinaSport()
    sports.telnet_sport_main()
#     sports.sport_parse_china(1)
#     telnet_news_sina()
