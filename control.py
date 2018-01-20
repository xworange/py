#coding:utf-8

#python 3版本
#砂E05 石E26 水泥E01 掺合料E10  外加剂E11

import time,os
import execute,netcode
import speak

def ini():#初始化
    #如果数据库里面没有合同编号信息，那么添加所有的合同编号。
    rs=speak.executeSQL("select conCreteProjectName from 混凝土供应信息")
    if rs.recordcount==0:
        allCompact=execute.reAllHntCompact()
        speak.pushHntCompactToDb(allCompact)
    #添加配合比
    rs=speak.executeSQL("select mixId from 设计配合比信息")
    if rs.recordcount==0:
        execute.saveAllAllHntMix()

    E='E05'
    rs=speak.executeSQL("select jcjgid from 原材料 where E='"+E+"'")
    if rs.recordcount==0:
        li=execute.reMaterialAlways(E)
        speak.pushMaterialToDb(li,E)

    E='E26'
    rs=speak.executeSQL("select jcjgid from 原材料 where E='"+E+"'")
    if rs.recordcount==0:
        li=execute.reMaterialAlways(E)
        speak.pushMaterialToDb(li,E)

    E='E1'
    rs=speak.executeSQL("select jcjgid from 原材料 where E='"+E+"'")
    if rs.recordcount==0:
        li=execute.reMaterialAlways(E)
        speak.pushMaterialToDb(li,E)

    E='E10'
    rs=speak.executeSQL("select jcjgid from 原材料 where E='"+E+"'")
    if rs.recordcount==0:
        li=execute.reMaterialAlways(E)
        speak.pushMaterialToDb(li,E)

    E='E11'
    rs=speak.executeSQL("select jcjgid from 原材料 where E='"+E+"'")
    if rs.recordcount==0:
        li=execute.reMaterialAlways(E)
        speak.pushMaterialToDb(li,E)

def control():
    while True:
        sCmd=str(speak.queryA())
        if sCmd!="":
            print(sCmd)
            if sCmd.find("平台任务单号")>-1:
                s=str(execute.rePlatformSerialNnumber())
                speak.commitB(s)
                print(s)
            if sCmd.find("提交单子")>-1:
                s=str(execute.pullList(sCmd))
                speak.commitB(s)
                print(s)

        time.sleep(0.3)

#===================================================================================


#print(reAllAllHntMix())
ini()

control()

#E='E11'
#di=execute.reMaterial(E)
#speak.pushMaterialToDb(di,E)
#for row in di:
#    print(row['jcjgId'])


