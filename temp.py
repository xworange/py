##coding:utf-8
#python 3版本  这个模块用于连接数据库
import netcode
import pypyodbc,os

#实例化数据库引擎
import win32com.client



conn = win32com.client.Dispatch(r'ADODB.Connection')
DSN = 'PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=D:/XW/python/business/py/db1.mdb;'
conn.Open(DSN)
#cur=conn.cursor()

'''
cur.execute("select * from 用户;")
rows = cur.fetchall()
print(rows)
'''