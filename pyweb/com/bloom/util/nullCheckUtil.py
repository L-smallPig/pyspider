# coding=utf8
'''
Created on 2017年9月7日

@author: Administrator
'''

def isNull(obj):
    if obj is None:
        return True
    else :
        return len(obj) <= 0

print isNull(3)
        
