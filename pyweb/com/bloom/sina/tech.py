# coding=utf8
'''
Created on 2017年9月11日

@author: Administrator
'''

import re
import urllib2

from bs4 import BeautifulSoup
import requests

import DateCheckUtil as dateUtil
import bizutil.DBNewsUtil as DBNewsUtil


class sinaTech(object):
    def sina_encode_soup(self, url):
        res=requests.get(url)
        res.encoding='UTF-8'

        # 使用剖析器为html.parser
        soup=BeautifulSoup(res.text, 'html5lib')
        return soup
    def tech_soup(self, url):
#     url = 'http://roll.finance.sina.com.cn/s/channel.php?ch=03#col=45&spec=&type=&ch=03&k=&offset_page=0&offset_num=0&num=60&asc=&page=1'
#     url = 'http://roll.finance.sina.com.cn/s/channel.php?ch=03#col=49&spec=&type=&ch=03&k=&offset_page=0&offset_num=0&num=60&asc=&page=1'
        response=urllib2.urlopen(url)
        data=response.read()

        soup=BeautifulSoup(data, 'html5lib')

        return soup
    def tech_soup_head(self, url):
#     url = 'http://roll.finance.sina.com.cn/s/channel.php?ch=03#col=45&spec=&type=&ch=03&k=&offset_page=0&offset_num=0&num=60&asc=&page=1'
#     url = 'http://roll.finance.sina.com.cn/s/channel.php?ch=03#col=49&spec=&type=&ch=03&k=&offset_page=0&offset_num=0&num=60&asc=&page=1'
        #创建请求头  
        headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "  
                              "(KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36",  
                 "Accept":"*/*"} 
        request = urllib2.Request(url,headers=headers) 
        response=urllib2.urlopen(request)
        data=response.read()

        soup=BeautifulSoup(data, 'lxml')

        return soup
    def tech_geturl_roll(self):
        # 基础页面 未添加下标
        baseUrl='http://tech.sina.com.cn/'
        # index 默认获取前十页数据
        urlList=[]

        soup=self.tech_soup_head(baseUrl)

#         中间概要
        middle=soup.select('.tech-mid .tech-news ul li a')
#         热点·动态获取
#         hot=soup.select('.cardlist-a__list')

        
        
        rmsg=self.tech_geturl_parse_soup(middle, '今日头条科技')
        if rmsg is not None:
            urlList.extend(rmsg)
        else:
            print '今日头条科技获取为空'

#
#         rmsg=self.tech_geturl_parse_soup(hot, '科技热点')
#         if rmsg is not None:
#             urlList.extend(rmsg)
#         else:
#             print '科技热点获取为空'
#
#         rmsg=self.tech_geturl_parse_soup(ndxw, '内地新闻')
#         if rmsg is not None:
#             urlList.extend(rmsg)
#         else:
#             print '内地新闻获取为空'


        print "Total:", len(urlList)
#         if len(localnews) > 0 :
#             for index in localnews:
#                     print index.text,index.get("href")
#                     urlList.append(index.get("href"))
#
#         else :
#             print '未定位到[内地新闻]'
        return urlList
    def tech_geturl_parse_soup(self, target, title):
        urlList=[]
        if target is not None and \
            len(target)>0  :
            for index in target :
#                 print index.text, index.get("href")
                urlList.append(index.get("href"))
        else:
            print '页面解析器为None：', title
        return urlList
    def tech_parse_local(self, url):
#         url='http://tech.sina.com.cn/it/2017-09-11/doc-ifykusey7592710.shtml'
#         url='http://tech.sina.com.cn/i/2017-09-11/doc-ifykuffc4979608.shtml'
#         url='http://news.sina.com.cn/c/nd/2017-09-11/doc-ifykusey7598389.shtml'
#         url = 'http://tech.sina.com.cn/t/2017-09-11/doc-ifykusey7693245.shtml'
#         url = 'http://tech.sina.com.cn/d/n/2017-09-11/doc-ifykusey8022496.shtml?cre=tianyi&mod=pctech&loc=3&r=25&doct=0&rfunc=54&tj=none&tr=25'
#         url = 'http://tech.sina.com.cn/i/2017-09-11/doc-ifykusey8010126.shtml?cre=tianyi&mod=pctech&loc=4&r=25&doct=0&rfunc=54&tj=none&tr=25'
        soup=self.tech_soup_head(url)
        body=soup.select('#artibody p')
        rarr=[]
#         print soup
#         print body
        if len(body)>0:
            for msg in body:
#                 print msg.text
                rarr.append(msg.text)
        else :
            print 'find artibody failed', url
            return None
        rmsg=''.join(rarr)
#         print rmsg
        return rmsg

    def tech_geturl_all(self):
#     urlList = finance_geturl_main_topMsg()
        urlList=self.tech_geturl_roll()
        print '页面捕获完毕，共计收集到地址：FINAL:', len(urlList)
        p_new=r'http://tech.sina.com.cn/[a-zA-Z]{1,4}/.*'

        rdicts={}
        print '=============开始匹配==============='

        for url in urlList :
    #         print ii
            if url is not None :

                if rdicts.has_key(url):
                    # 重复url，不再请求
                    continue
                if re.match(p_new, url, re.M) is not None :
                    vmsg=self.tech_parse_local(url)
                else:
                    print '暂未匹配该路径', url
                    continue

                if vmsg is not None :
                    rdicts[url]=vmsg
            else :
                print 'URL为None 跳过'
        print '结果集如下', len(rdicts)
        for k, v in rdicts.items():
            print k

        return rdicts
    def telnet_tech_main(self):
        mydb=DBNewsUtil.DBNews()

        rdicts=self.tech_geturl_all()
        length=len(rdicts)
        if length<5 :
            print '结果集太少', str(length)
            return
        existLen=0
        if(length>0) :
            print '成功捕获访问地址个数：', length
            taskNum=mydb.getNextVal()
            for rUrl, rMsg in rdicts.items():
                print rUrl
                param={"news_url":rUrl}
                isexist=mydb.isExistNewsMsg(param)
                if isexist:
                    existLen+=1
                else:
                    news_date=dateUtil.currDateFormateA()
                    param={'news_task':taskNum,
                               'news_date':news_date,
                               'news_url':rUrl,
                               'news_message':rMsg,
                               'news_scope':'technology'}
                    mydb.saveNews(param)

            currDate=dateUtil.currDateFormate()
            comment=''
            if existLen>0:
                comment='存在'+str(existLen)+'/'+str(length)+',短时间内重复请求.'
            else:
                comment='SUCCESS'
            param={'newslog_task':taskNum, 'newslog_date':currDate, 'newslog_count':length, 'newslog_comment':comment}
            mydb.saveNewslog(param);
        print '成功处理完毕！'
if __name__=="__main__":

    sports=sinaTech()
#     sports.tech_geturl_roll()
#     sports.tech_parse_local(1)
#     sports.sport_parse_national(1)
    sports.telnet_tech_main()
