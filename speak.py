#coding:utf-8
#python 3版本  这个模块用于连接数据库
import netcode
import os
import win32com.client

'''
def reCur():
    accdb1 = os.path.dirname(__file__)+"/db1.mdb"
    print (accdb1)
    conn = pypyodbc.connect(u'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + accdb1)
    print('数据库连接成功')
    return conn.cursor()
cur=reCur()
'''
conn = win32com.client.Dispatch(r'ADODB.Connection')
conn.Open('PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE='+os.path.dirname(__file__)+"/db1.mdb")


def executeSQL(sSQL):
    rs = win32com.client.Dispatch(r'ADODB.Recordset')
    st=sSQL.split()[0].lower()
    if st=='insert' or st=='delete' or st=='update':
        rs.Open(sSQL, conn, 1, 3)
    else:
        rs.CursorLocation = 3
        rs.Open(sSQL, conn, 1, 3)
        return rs

def reuserName():
    rs=executeSQL("select * from 用户;")
    return rs

def queryA():#和VB沟通 a
    cur.execute("select a from communi WHERE 主键=1;")
    rows = cur.fetchall()
    return str(rows[0])



def commitB(S): #和VB沟通 b
    cur.execute("UPDATE communi SET b=\'"+ S + "\' WHERE 主键=1;")
    cur.execute("UPDATE communi SET a=\'\' WHERE 主键=1;")
    cur.commit()

def addSem(s):#添加分号，好导入数据库
    s=str(s)
    s=s.replace("\'","")
    return "\'"+s+"\'"
def addSemComma(s):#添加分号和逗号
    return addSem(s)+","



def pushHntCompactToDb(allCompact):
    for row in allCompact:
        #print(row)
        st="INSERT INTO 混凝土供应信息 (buildUnit,compactAddress,conCreteCompactId,conCreteCompactPid,conCreteProjectCode,conCreteProjectName,hntpermissionIds,inSpectInstituTionName,qualityName,signingDataStr) VALUES (" + addSemComma( row ['buildUnit'])   +addSemComma(row['compactAddress'])+addSemComma(row['conCreteCompactId'])+addSemComma(row['conCreteCompactPid'])+addSemComma(row['conCreteProjectCode'])+addSemComma(row['conCreteProjectName'])+addSemComma(row['hntpermissionIds'])+addSemComma(row['inSpectInstituTionName'])+addSemComma(row['qualityName'])+addSem(row['signingDataStr'])+")"
        print(st)
        cur.execute(st)
        #print("INSERT INTO 混凝土供应信息 VALUES (" +addSem(row['buildUnit'])  +addSem(row['compactAddress'])+addSem(row['conCreteCompactId'])+addSem(row['conCreteCompactPid'])+addSem(row['conCreteProjectCode'])+addSem(row['conCreteProjectName'])+addSem(row['hntpermissionIds'])+addSem(row['inSpectInstituTionName'])+addSem(row['qualityName'])+addSem(row['signingDataStr']) +")")
    cur.commit()

#rst=executeSQL('Select * from 混凝土供应信息')
#print(rst[2])
rs=reuserName()
print(rs.fields.item(2).value)
