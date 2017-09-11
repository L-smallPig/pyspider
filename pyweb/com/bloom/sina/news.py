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


class sinaNews(object):
    def sina_encode_soup(self,url):
        res = requests.get(url)
        res.encoding = 'UTF-8'
        
        # 使用剖析器为html.parser
        soup = BeautifulSoup(res.text, 'html5lib')
        return soup
    def news_soup(self,url):
#     url = 'http://roll.finance.sina.com.cn/s/channel.php?ch=03#col=45&spec=&type=&ch=03&k=&offset_page=0&offset_num=0&num=60&asc=&page=1'
#     url = 'http://roll.finance.sina.com.cn/s/channel.php?ch=03#col=49&spec=&type=&ch=03&k=&offset_page=0&offset_num=0&num=60&asc=&page=1'
        response = urllib2.urlopen(url)
        data = response.read()
        
        soup = BeautifulSoup(data, 'html5lib')
    
        return soup
    def news_geturl_roll(self):
        #基础页面 未添加下标
        baseUrl = 'http://news.sina.com.cn/'
        #index 默认获取前十页数据
        urlList = []

        soup = self.sina_encode_soup(baseUrl)
            
#         国内新闻
        gnxw = soup.select('#blk_new_gnxw .blk_09 ul li a') 
#         国际新闻
        gjxw = soup.select('#blk_gjxw_01 ul li a')
#         社会新闻
        sh = soup.select('#blk_sh_01 ul li a')
#         内地新闻
        ndxw = soup.select('#blk_ndxw_01 ul li a')
#         军事新闻
#         jsxw = soup.select('#blk_jsxw_02 ul li a')
        
        
        rmsg = self.news_geturl_parse_soup(gnxw,'国内新闻')
        if rmsg is not None:
            urlList.extend(rmsg)
        else:
            print '国内新闻获取为空'
            
            
        rmsg = self.news_geturl_parse_soup(gjxw,'国际新闻')
        if rmsg is not None:
            urlList.extend(rmsg)
        else:
            print '国际新闻获取为空'
            
        rmsg = self.news_geturl_parse_soup(sh,'社会新闻')
        if rmsg is not None:
            urlList.extend(rmsg)
        else:
            print '社会新闻获取为空'
            
        rmsg = self.news_geturl_parse_soup(ndxw,'内地新闻')
        if rmsg is not None:
            urlList.extend(rmsg)
        else:
            print '内地新闻获取为空'
            
        
        print "Total:",len(urlList)
#         if len(localnews) > 0 :
#             for index in localnews:
#                     print index.text,index.get("href")
#                     urlList.append(index.get("href"))
#             
#         else :
#             print '未定位到[内地新闻]'
        return urlList
    def news_geturl_parse_soup(self,target,title):
        urlList = []
        if target is not None and \
            len(target) > 0  :
            for index in target :
#                 print index.text,index.get("href")
                urlList.append(index.get("href"))
        else:
            print '页面解析器为None：',title
        return urlList
    def sport_parse_local(self,url):
#         url = 'http://news.sina.com.cn/c/nd/2017-09-11/doc-ifykusey7623059.shtml'
#         url = 'http://news.sina.com.cn/o/2017-09-11/doc-ifyktzim9473561.shtml'
#         url = 'http://news.sina.com.cn/w/2017-09-09/doc-ifyktzim9020274.shtml'
#         url = 'http://news.sina.com.cn/w/sy/2017-09-11/doc-ifyktzim9426977.shtml'
#         url = 'http://news.sina.com.cn/s/wh/2017-09-11/doc-ifyktzim9455811.shtml'
#         url = 'http://news.sina.com.cn/c/nd/2017-09-11/doc-ifykusey7598389.shtml'
        
        soup = self.sina_encode_soup(url)
        body = soup.select('#artibody')
        rarr = []
        if len(body)>0:
            pmsg = body[0].select('p')
            for msg in pmsg:
#                 print msg.text 
                rarr.append(msg.text)
        else :
            print 'find artibody failed',url
            return None
        rmsg = ''.join(rarr)   
    #         print rmsg
        return rmsg

    def news_geturl_all(self):
#     urlList = finance_geturl_main_topMsg()
        urlList = self.news_geturl_roll()
        print '页面捕获完毕，共计收集到地址：FINAL:',len(urlList)
        
        p_new  = r'http://news.sina.com.cn/[a-zA-Z]/.*'
        
        rdicts = {}
        print '=============开始匹配==============='
        
        for url in urlList :
    #         print ii
            if url is not None :
                
                if rdicts.has_key(url):
                    #重复url，不再请求
                    continue
                if re.match(p_new, url, re.M) is not None :
                    vmsg = self.sport_parse_local(url)
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
    def telnet_news_main(self):
        mydb = DBNewsUtil.DBNews()
        
        rdicts = self.news_geturl_all()
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
                               'news_scope':'news'}
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
    
    sports = sinaNews()
    sports.telnet_news_main()
#     sports.sport_parse_local(1)
#     sports.sport_parse_national(1)
#     sports.news_geturl_all()
