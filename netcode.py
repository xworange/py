#coding:utf-8
#python 3版本

import codecs,os,time,datetime


def readfile(path):
    with codecs.open(path) as f:
        return f.read()

def writefile(path,s):
    with open(path, 'w') as f:
        f.write(s)


def returnParentPath(): #返回当前目录的父目录
    d = os.path.dirname(__file__)
    parent_path = os.path.dirname(d) #获得d所在的目录,即d的父级目录
    return parent_path

def reNday(n): #返回N天前的字符串
    t= datetime.datetime.now() + datetime.timedelta(days=-n)
    s=str(t.year)+'-'+str(t.month)+'-'+str(t.day)
    return s

def reToday():
    t= datetime.datetime.now()
    s=str(t.year)+'-'+str(t.month)+'-'+str(t.day)
    return s