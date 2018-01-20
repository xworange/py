#coding:utf-8
#python 3版本  这个模块用于连接数据库
import netcode
import os
import win32com.client

conn = win32com.client.Dispatch(r'ADODB.Connection')
conn.Open('PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE='+os.path.dirname(__file__)+"/db1.mdb")

#A将请求数据写到文件a.txt，写完后改名为aa.txt,  B发现aa.txt存在时，读取其内容，调用相应功能，将结果写到文件b.txt，写完后删除aa.txt，改名为bb.txt
#A发现bb.txt存在时，读取其内容，读完后删除bb.txt
aaFile=netcode.returnParentPath()+'\\aa.txt'
bFile=netcode.returnParentPath()+'\\b.txt'
bbFile=netcode.returnParentPath()+'\\bb.txt'

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
    #rs=executeSQL("select a from communi WHERE 主键=1;")
    #return rs.fields.item(0).value
    if os.path.exists(aaFile):
        return netcode.readfile(aaFile)
    else:
        return ""



def commitB(S): #和VB沟通 b
    #executeSQL("UPDATE communi SET b=\'"+ S + "\' WHERE 主键=1;")
    #executeSQL("UPDATE communi SET a=\'\' WHERE 主键=1;")
    netcode.writefile(bFile,S)
    os.remove(aaFile)
    os.rename( bFile,bbFile )

def addSem(s):#添加分号，好导入数据库
    s=str(s)
    s=s.replace("\'","")
    return "\'"+s+"\'"
def addSemComma(s):#添加分号和逗号
    return addSem(s)+","



def pushHntCompactToDb(allCompact):  #混凝土供应信息 写入数据库
    for row in allCompact:
        #print(row)
        st="INSERT INTO 混凝土供应信息 (buildUnit,compactAddress,conCreteCompactId,conCreteCompactPid,conCreteProjectCode,conCreteProjectName,hntpermissionIds,inSpectInstituTionName,qualityName,signingDataStr) VALUES (" + addSemComma( row ['buildUnit'])   +addSemComma(row['compactAddress'])+addSemComma(row['conCreteCompactId'])+addSemComma(row['conCreteCompactPid'])+addSemComma(row['conCreteProjectCode'])+addSemComma(row['conCreteProjectName'])+addSemComma(row['hntpermissionIds'])+addSemComma(row['inSpectInstituTionName'])+addSemComma(row['qualityName'])+addSem(row['signingDataStr'])+")"
        print(st)
        executeSQL(st)



def pushMaterialToDb(allM,reportType):  #原材料信息 写入数据库
    for row in allM:
        #print(row)
        st="INSERT INTO 原材料 (inspectInstitutionName,reportId,nodeName,jcjgid,E) VALUES  (" \
           + addSemComma( row ['inspectInstitutionName'])   +addSemComma(row['reportId'])+addSemComma(row['nodeName'])+addSemComma(row['jcjgId']) \
           +addSem(reportType)+")"
        print(st)
        executeSQL(st)

def reReportId(key):
    if key=="null":
        return ""
    else:
        rs=executeSQL("select * from 原材料 where 主键 like "+addSem(key))
        return rs.fields.item(2).value

#rs=reuserName()
#print(rs.fields.item(2).value)
#print(rs.fields.count)
#print(queryA())
#print(reReportId(178))
