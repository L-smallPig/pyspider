# coding=utf-8
'''
Created on 2017年9月3日

@author: Administrator
'''
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import urllib
import os

import html5lib
from html5lib import sanitizer
from html5lib import treebuilders

def before_getBaseUrl():
    url = 'http://finance.sina.com.cn/fund/'
    
    res = requests.get(url)
    # 使用UTF-8编码
    res.encoding = 'UTF-8'
    
    # 使用剖析器为html.parser
    soup = BeautifulSoup(res.text, 'html.parser')
    
    #     定义真正访问 地址集合
    urlList = []
    
    print 'Here we go :'
    # 遍历每一个class=news-item的节点
    for news in soup.select('.p02_m'):
        h3 = news.select('.fbold')
#         #只选择长度大于0的结果
        if len(h3) > 0:
#             #新闻时间
            for aa in h3 :
                alist = aa.select('a')
                for eachA in alist :
#                 print tabA
                    href = eachA.attrs.get('href')
                    urlList.append(href)
#                     print href
    return urlList
def dual_parseUrlMsg(url):
    '''
                    待处理
                   该URL入库
                   每次处理前，查库，存在则不再重复录入
                    
    '''
#     url = 'http://finance.sina.com.cn/fund/'
    
#     url = 'http://finance.sina.com.cn/roll/2017-09-04/doc-ifykpzey4095098.shtml'
    res = requests.get(url)
    # 使用UTF-8编码
    res.encoding = 'UTF-8'
    filename = 'demo'+url+'.txt'
    filename = 'demo.txt'
    fp = open(filename,'a+') 
    
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
                    print msg
                    fp.write(msg)
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
    
    fp.closed
        
#     return urlList
def telnetdemo():
    url = 'http://finance.sina.com.cn/roll/2017-09-04/doc-ifykpzey4095098.shtml'
    fp = urllib.urlopen(url)
    # Create an html5lib parser. Not sure if the sanitizer is required.
    parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("beautifulsoup"), tokenizer=sanitizer.HTMLSanitizer)
    # Load the source file's HTML into html5lib
    html5lib_object = parser.parse('')
    # In theory we shouldn't need to convert this to a string before passing to BS. Didn't work passing directly to BS for me however.
    html_string = str(html5lib_object)
    
    # Load the string into BeautifulSoup for parsing.
    soup = BeautifulSoup(html_string)
    
    for content in soup.findAll('div'):
        print content
def telnet():
    
    urlList = before_getBaseUrl()
    length = len(urlList)
    if(length > 0) :
        print '成功捕获访问地址个数：', length
        for index in range(len(urlList)):
            print '开始处理：',index+1,'/',len(urlList)
            print urlList[index]
#             dual_parseUrlMsg(urlList[index])
#         for url in urlList:
#             dual_parseUrlMsg(url)
#             print url
    else:
        print '未获取到查询地址'
   
    
telnet()
# dual_parseUrlMsg('a')

# url = 'http://finance.sina.com.cn/roll/2017-09-04/doc-ifykpzey4095098.shtml'
# page = urllib.urlopen(url)
# soup = BeautifulSoup(page.read(), 'html5lib')
# links = soup.findAll('a')
# 
# for link in links:
#     print(link.string, link['href'])
