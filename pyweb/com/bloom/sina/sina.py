# coding=utf-8
'''
Created on 2017年9月3日

@author: Administrator
'''

import re

from bs4 import BeautifulSoup
import requests

import DateCheckUtil as dateUtil
import bizutil.DBNewsUtil as DBNewsUtil
import sys
type = sys.getfilesystemencoding()


def sinasoup():
    url = 'http://finance.sina.com.cn'
    res = requests.get(url)
    res.encoding = 'UTF-8'
    
    # 使用剖析器为html.parser
    soup = BeautifulSoup(res.text, 'html5lib')
    return soup
def sinasoup_roll(url):
#     url='http://roll.finance.sina.com.cn/s/channel.php?ch=03#col=45&spec=&type=&ch=03&k=&offset_page=0&offset_num=0&num=80&asc=&page=1'
    res = requests.get(url)
    res.encoding = 'utf-8'
#     res.decode('UTF-8').encode(type)
#     print res.headers.get('Content-Encoding')
#     res.headers('Accept-encoding', 'gzip')
    # 使用剖析器为html.parser
    soup = BeautifulSoup(res.text, 'html5lib')
#     html.parser
    
    
    return soup
'''获取新浪新闻基础请求路径 170905
'''
def finance_geturl_fundtopMsg():
    url = 'http://finance.sina.com.cn/fund/'
    
    res = requests.get(url)
    res.encoding = 'UTF-8'
    # 使用剖析器为html.parser
    soup = BeautifulSoup(res.text, 'html.parser')
    #     定义真正访问 地址集合
    urlList = []
    print 'Here we go :'
    # 遍历每一个class=news-item的节点
    for news in soup.select('.p02_m'):
#       获取大标题内容
        h3 = news.select('.fbold')
        #获取摘要模块
        abstract = news.select('.list01')
        
        if len(h3) > 0:
#             #新闻时间
            for aa in h3 :
                alist = aa.select('a')
                for eachA in alist :
#                 print tabA
                    href = eachA.attrs.get('href')
                    print eachA.text
                    urlList.append(href)
#                     print href
        if len(abstract) > 0 :
            absTitle = abstract[0]
            absLi = absTitle.select('li')
            for li in absLi :
                li_a = li.select('a')
                for aa in li_a :
                    href = aa.attrs.get('href') 
                    print aa.text,":",href
                    urlList.append(href)
    return urlList
'''新浪财经 抓站要闻 
'''
def finance_geturl_main_topMsg():
    soup = sinasoup()
    
    #     定义真正访问 地址集合
    urlList =[]
    
    div_direct =  soup.select('#directAd_huaxia')
    if len(div_direct)>0 :
        
        #part1 要闻
        alist = div_direct[0].select("#impNews1 #fin_tabs0_c0 .m-p1-mb1-list ul li a")
        for aa in alist :
#             print aa.text,":",aa.get("href")
            urlList.append(aa.get("href"))
        #part2 证券内容
        alist2 = div_direct[0].select(".m-p1-m-blk2 .m-p1-mb2-list #directAd_dell_fidx_02,#directAd_dell_fidx_03  li a")
        for a2 in alist2 :
#             print a2.text,":",a2.get("href")
            urlList.append(a2.get("href"))
            
        alist3 = div_direct[0].select(".m-p1-m-blk2 .m-p1-mb2-list #directAd_dell_fidx_05,#directAd_dell_fidx_04  li a")
        for a3 in alist3 :
#             print a23text,":",a2.get("href")
            urlList.append(a3.get("href"))
    else:
        print '未定位到【抓站内容】'
    
    return urlList
def finance_geturl_roll():
    #基础页面 未添加下标
    baseUrl = 'http://roll.finance.sina.com.cn/s/channel.php?ch=03#col=43&spec=&type=&ch=03&k=&offset_page=0&offset_num=0&num=60&asc=&page='
    #index 默认获取前十页数据
    sum = 5
    soup = None 
    urlList = []
    for index in range(0,sum) :
        url = baseUrl+str(index+1)
        soup = sinasoup_roll(url)
        dlist = soup.select('#pL_Main #d_list')
        if len(dlist) > 0 :
            alist = dlist[0].select('.c_tit a')
#             alist = dlist[0].select('ul li .c_tit a')
#             print len(alist)
            for a2 in alist :
#                 print ss.text 
#                 print a2.get("href")
                urlList.append(a2.get("href"))
#                 print a2.get('href')
#                 print a2.text.decode('utf-8').incode('mbcs'),':',a2.get('href')
            
            
        else :
            print '未定位到结果集合'
    print '页面捕获完毕'
    return urlList
#         soup = sinasoup_roll(url)
    
def finance_geturl_all():
#     urlList = finance_geturl_main_topMsg()
    urlList = finance_geturl_roll()
    print '页面捕获完毕，共计收集到地址：FINAL:',len(urlList)
    
    p_roll  = 'http://finance.sina.com.cn/roll/\\d{4}-\\d{1,2}-\\d{1,2}/'
    p_blog  = r'http://blog.sina.com.cn/s/.*'
    p_top   = r'http://cj.sina.cn/article/detail/.*'
    p_stock = r'http://finance.sina.com.cn/stock/(t|hkstock)/.*'
    
    
    rdicts = {}
    print '=============开始匹配==============='
    
    # blog 滚动条
    for rollurl in urlList :
    #         print ii
        if rollurl is not None and re.match(p_roll, rollurl, re.M) is not None:
            #保存博客内容
    #             print stockurl
            if rdicts.has_key(rollurl):
                #重复url，不再请求
                continue
            vmsg = finance_parse_top_stock(rollurl)
            if vmsg is not None :
                rdicts[rollurl] = vmsg
    
    # blog 港股
    for stockurl in urlList :
#         print ii
        if stockurl is not None and re.match(p_stock, stockurl, re.M) is not None:
            #保存博客内容
#             print stockurl
            if rdicts.has_key(stockurl):
                #重复url，不再请求
                continue
            vmsg = finance_parse_top_stock(stockurl)
            if vmsg is not None :
                rdicts[stockurl] = vmsg
    # blog 收录
    for blogurl in urlList :
#         print ii
        if blogurl is not None and re.match(p_blog, blogurl, re.M) is not None:
            #保存博客内容
            print blogurl
            if rdicts.has_key(blogurl):
                #重复url，不再请求
                continue
            vmsg = finance_parse_top_blog(blogurl)
            if vmsg is not None :
                rdicts[blogurl] = vmsg
    # 财经首页
    for topurl in urlList :
#         print ii
        if topurl is not None and re.match(p_top, topurl, re.M) is not None:
            #保存财经内容
            print topurl
            if rdicts.has_key(topurl):
                #重复url，不再请求
                continue
            vmsg = finance_parse_top_cj(topurl)
            if vmsg is not None :
                rdicts[topurl] = vmsg
    
    print '======赛选后的去重内容======共计条数：',len(rdicts)
    for k,v in rdicts.items():
        print k  
    return rdicts

#新浪博客内容获取 滚动
def finance_parse_top_roll(url):
    url = 'http://finance.sina.com.cn/roll/2017-09-05/doc-ifykpzey4381548.shtml'
    soup = sinasoup_roll(url)
    body = soup.select('#articlebody #sina_keyword_ad_area2')
    rarr = []
    if len(body)>0:
        pmsg = body[0].select('p')
        for msg in pmsg:
            rarr.append(msg.text)
#             print msg.text 
    else :
        print 'find artibody failed'
    rmsg = ''.join(rarr)   
    return rmsg
#新浪博客内容获取
def finance_parse_top_blog(url):
#     url = 'http://blog.sina.com.cn/s/blog_6fe7ef8d0102xe9z.html'
    soup = sinasoup_roll(url)
    body = soup.select('#articlebody #sina_keyword_ad_area2')
    rarr = []
    if len(body)>0:
        pmsg = body[0].select('p')
        for msg in pmsg:
            rarr.append(msg.text)
#             print msg.text 
    else :
        print 'find artibody failed'
    rmsg = ''.join(rarr)   
    return rmsg
#新浪博客内容获取》港股
def finance_parse_top_stock(url):
#     url = 'http://finance.sina.com.cn/stock/hkstock/ggscyd/2017-09-06/doc-ifyktzim8380896.shtml'
#     url = 'http://finance.sina.com.cn/stock/t/2017-09-06/doc-ifykuftz4967502.shtml'
#     url = 'http://finance.sina.com.cn/stock/hkstock/ggscyd/2017-09-06/doc-ifyktzim8386365.shtml'
    url = 'http://finance.sina.com.cn/roll/2017-09-05/doc-ifykpzey4381548.shtml'
    soup = sinasoup_roll(url)
    body = soup.select('#articleContent #artibody')
    rarr = []
    if len(body)>0:
        pmsg = body[0].select('p')
        for msg in pmsg:
            rarr.append(msg.text)
#             print msg.text 
    else :
        print 'find artibody failed'
    rmsg = ''.join(rarr)  
#     print rmsg
    return rmsg
#财经首页内容获取
def finance_parse_top_cj(url):
    soup = sinasoup_roll(url)
    body = soup.select('#articleContent #artibody')
    rarr = []
    if len(body)>0:
        pmsg = body[0].select('p')
        for msg in pmsg:
            rarr.append(msg.text)
#             print msg.text 
    else :
        print 'find artibody failed'
        
    return ''.join(rarr)
    
    
'''获取新浪新闻根据请求地址获取信息入库 170905
'''
def finance_parse_fundtopMsg(url):
    
    res = requests.get(url)
    # 使用UTF-8编码
    res.encoding = 'UTF-8'
#     filename = 'demo'+url+'.txt'
#     filename = 'demo.txt'
#     fp = open(filename,'a+') 
#     
    # 结果集，返回
    rMsg = ''
    
    # 使用剖析器为html.parser
    soup = BeautifulSoup(res.text, 'html5lib')
    article = soup.select("#articleContent")
    if(len(article) > 0):
        print '成功定位到：content'
        artibody = article[0].select("#artibody")
        if(len(artibody)>0):
            print '成功定位到：content>body'
            divs = artibody[0].select("p")
            if(len(divs)>0):
                print '开始读取段落信息：'
                '''
                                                            文本解析处理START
                '''
                for div in divs:
                    msg = div.text
                    rMsg = rMsg + ''.join(msg)
#                     print msg
#                     fp.write(msg)
                '''
                                                             文本解析处理 END
                '''
            else:
                print '未查询到文本信息'
        else:
            print 'HTML 格式变更，未查找到content>body'
            return
    else:
        print 'HTML 格式变更，未查找到content'
        return 
    
#     fp.closed
    
    return rMsg    


def telnet_finance_main():
    mydb = DBNewsUtil.DBNews()
    
    rdicts = finance_geturl_all()
    length = len(rdicts)
    
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
                           'news_scope':'finance'}
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
                
            
        
        
        
def telnet_news_sina():
    mydb = DBNewsUtil.DBNews()
    
    urlList = finance_geturl_fundtopMsg()
    
    length = len(urlList)
    if len(urlList)>0:
        print '捕获数据累计：'+str(length)
    else:
        print '未捕获到数据'
    succLen = 0
    failLen = 0
    existLen= 0
    if(length > 0) :
        print '成功捕获访问地址个数：', length
        mydb = DBNewsUtil.DBNews()
        taskNum = mydb.getNextVal()
        
        
        for index in range(len(urlList)):
            print '开始处理：',index+1,'/',len(urlList)
            url = urlList[index]
            param={"news_url":url}
            isexist = mydb.isExistNewsMsg(param)
            if isexist :
                existLen+=1
                #存在记录 不再保存
                print '存在该路径：',url
            else :
                #路径地址请求访问
                rMsg = finance_parse_fundtopMsg(urlList[index])
                
                '''   pa_voice_news 解析保存   STAET             '''
                if rMsg is None or not rMsg.strip():
                    print '请求内容为空'
                    failLen+=1
                else:
                    succLen+=1
#                     news_task,news_date,news_url,news_message
                    news_date = dateUtil.currDateFormateA()
                    param={'news_task':taskNum,
                           'news_date':news_date,
                           'news_url':url,
                           'news_message':rMsg,
                           'news_scope':'finance'}
                    mydb.saveNews(param)
                    print rMsg
                '''   pa_voice_news 解析保存   STAET             '''
        #save news log 
        '''   pa_voice_newslog 解析保存   STAET             '''
        currDate = dateUtil.currDateFormate()
        comment = ''
        if failLen > 0 :
            comment +='失败'+str(failLen)+'/'+str(length)+',请求失败或访问地址无效.'
            
        if existLen > 0 :
            comment +='存在'+str(existLen)+'/'+str(length)+',短时间内重复请求.'    
            
        if succLen ==0 :
            comment += '其它短时间内重复访问！'
        elif succLen < length :
            comment += '成功'+str(succLen)+'/'+str(length)+',存在部分请求信息获取失败.'
        else:
            comment += 'SUCCESS'
            
        param={'newslog_task':taskNum,'newslog_date':currDate,'newslog_count':length,'newslog_comment':comment}
        mydb.saveNewslog(param);         
        '''   pa_voice_newslog 解析保存   STAET             '''    
    else:
        print '未获取到查询地址'


if __name__ == "__main__":
    
    
    telnet_news_sina()
#     telnet_finance_main()
#     finance_geturl_roll()
#     finance_parse_top_blog(1)
#     finance_parse_top_stock(1)

#     finance_geturl_all()