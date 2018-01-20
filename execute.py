#coding:utf-8
#python 3  这个模块用于跟网站沟通
import datetime,time,os

import urllib,speak,netcode
from PIL import Image
from http.cookiejar import *
from urllib.request import *

def returnNewCookie():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
        }
    
    cookie = MozillaCookieJar(os.path.dirname(__file__)+'\cookie.txt')
    CaptchaUrl = "http://117.27.135.9:8083/sospweb//servlet/VerificationCode"
    PostUrl = "http://117.27.135.9:8083/sospweb/login/loginAction!userLogin.do"
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    rs=speak.reuserName()
    username =rs.Fields.item(0).value
    password = rs.Fields.item(1).value
    # 用户名和密码
    picture = opener.open(CaptchaUrl).read()
    # 用openr访问验证码地址,获取cookie
    local = open('c:\\image.jpg', 'wb')
    local.write(picture)
    local.close()
    image =Image.open('c:\\image.jpg')
    image.show()
    # 保存验证码到本地
    SecretCode = input('输入验证码： ')
    # 打开保存的验证码图片 输入
    postData = {
    'userAccount': username,
    'password': password,
    'code': SecretCode,
    }
            # 根据抓包信息 构造表单
    # 根据抓包信息 构造headers
    #data = urllib.parse.urlencode(postData)
    data = urllib.parse.urlencode(postData).encode(encoding='UTF8')
    # 生成post数据 ?key1=value1&key2=value2的形式
    request = Request(PostUrl, data, headers)
    # 构造request请求
    response = opener.open(request)
    result = response.read()
    result=result.decode('utf-8')
    print('longin:'+result)
    if result.find('用户名')==-1:
        print('手动输入验证码登录成功')
        cookie.save('cookie.txt',ignore_discard=True, ignore_expires=True)
        return cookie
    else:
        print('手动输入验证码登录失败')

def returnCookie():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
        }
    cookie = MozillaCookieJar(os.path.dirname(__file__)+'\cookie.txt')

    if os.path.exists(os.path.dirname(__file__)+'\cookie.txt'):
        #print("cookie存在")
        cookie.load(ignore_discard=True, ignore_expires=True)
        handler = urllib.request.HTTPCookieProcessor(cookie)
        opener = urllib.request.build_opener(handler)
        rs=speak.reuserName()
        jcjg=rs.Fields.item(2).value
        postData={
            'jcjgId':jcjg
        }
        PostUrl="http://117.27.135.9:8083/sospweb/com/zr/porminrTask/porminrTaskAction!getProductionTaskId.do"
        data = urllib.parse.urlencode(postData).encode(encoding='UTF8')
        request = Request(PostUrl, data, headers)
        response = opener.open(request)
        result = response.read()
        result=result.decode('utf-8')
        #print(result)
        if result.find('当前用户的会话已过期，请重新登录')==-1:
            print('旧cookie登录成功')
            return cookie
        else:
            return returnNewCookie()
    else:

        return returnNewCookie()
def unitToDB():  #把单位名称填入数据库
    rs=speak.reuserName()
    if rs.fields.item(3).value==None:
        ss=post("http://117.27.135.9:8083/sospweb/com/zr/frame/toppanel.jsp",{})
        istart=ss.find("登录单位：")
        iend=ss.find("|",istart)
        print(ss[istart:iend])
        istart=istart+5
        st=ss[istart:iend]
        st=st.strip()
        userName=rs.fields.item(0).value
        speak.executeSQL("UPDATE 用户 SET unit=\'"+ st + "\' WHERE userName=\'"+userName+"\'")


def returnOpener():
    cookie = returnCookie()
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = build_opener(handler)
    unitToDB()  #把单位名称填入数据库
    return opener

opener=returnOpener()


def post(PostUrl, data):
    #所有的请求从这里发出去。
    headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Language': 'zh-CN,zh;q=0.8',
'Connection': 'keep-alive',
'Content-Type': 'application/x-www-form-urlencoded',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
}
    #data = urllib.parse.urlencode(data)
    data = urllib.parse.urlencode(data).encode(encoding='UTF8')
    request = Request(PostUrl, data, headers)
    response = opener.open(request)
    return response.read().decode('utf-8')


'''
def returnStartTime():
    #返回起始时间，用于向服务器请求数据
    if datetime.datetime.now().hour>8:
        return  time.strftime('%Y-%m-%d',time.localtime(time.time()))
    else:
        t= datetime.datetime.now() + datetime.timedelta(days=-1)
        s=str(t.year)+'-'+str(t.month)+'-'+str(t.day)
        return s

def pleaseData():   #向服务器请求数据
    txtlist=[]
    curPage=1
    user=speak.reUserName()
    company = user[0][2]
    while True:
        postData = {
    'tjcjgid':company,#'JC553240071',
    #'inspectInstitutionName' :'华润混凝土（龙岩）有限公司',
    'startTime2': returnStartTime(),
    'nentTime2':  time.strftime('%Y-%m-%d',time.localtime(time.time())),
    'curPage':str(curPage)
    }
        PostUrl='http://117.27.135.9:8083/sospweb/com/zr/hnttask/hnttaskAction!queryAllHntTask.do'
        result =post(PostUrl,postData)

        if len(result)<200:
            return txtlist
            break
        else:
            print('第'+str(curPage)+'页数据请求成功')
            txtlist.append(result)
            curPage+=curPage
            time.sleep(0.1)
'''

def rePlatformSerialNnumber():#返回平台任务单号：
    rs=speak.reuserName()
    jcjg=rs.Fields.item(2).value
    s=post('http://117.27.135.9:8083/sospweb/com/zr/porminrTask/porminrTaskAction!getProductionTaskId.do',{'jcjgId':jcjg})
    s=s.replace('true','\'true\'')
    di=eval(s)
    return di['message']


def reAllHntCompact():#返回所有的合同编号 List形式返回
    s=post('http://117.27.135.9:8083/sospweb/com/zr/hntcompact/hntcompactAction!queryAllHntCompact.do',{'curPage':'1'})
    if len(s)<100:
        return "失败，没有查询到任何合同编号."
    #print(s)
    #s=s.replace('true','\'true\'')
    di=eval(s)
    totalPage=int(di['totalPage'])
    allCompact=[]
    for i in range(1,totalPage+1):
        print('合同编号信息读取第几页：'+str(i))
        s=post('http://117.27.135.9:8083/sospweb/com/zr/hntcompact/hntcompactAction!queryAllHntCompact.do',{'curPage':str(i)})
        di=eval(s)
        di=di['dataList']
        #print(di)
        for row in di:
            allCompact.append(row)
    return allCompact

#
def saveAllAllHntMix():#数据量大，查到配合比直接进数据库
    s=post('http://117.27.135.9:8083/sospweb/com/zr/hntmix/hntmixAction!queryAllHntMix.do',{'curPage':'1'})
    if len(s)<100:
        return "失败，没有查询到任何配合比信息."
    di=eval(s)
    totalPage=int(di['totalPage'])
    allMix=[]
    for i in range(1,totalPage+1):
        print('配合比信息读取第几页：'+str(i))
        s=post('http://117.27.135.9:8083/sospweb/com/zr/hntmix/hntmixAction!queryAllHntMix.do',{'curPage':str(i)})
        di=eval(s)
        di=di['dataList']
        #print(di)
        for row in di: #变量太大，所以直接进入数据库。
            #print(row)
            #allMix.append(row)

            st="INSERT INTO 设计配合比信息 (additive1,additive2,additive3,additive4,\
              admixtrue1,admixtrue2,admixtrue3,cement,isBig,impervious,mixGrade,mixId,mixPid,sand,stone,water,zmixGrade,inSpectInstituTionName) VALUES ("\
               +speak.addSemComma(row ['additive1'])  +speak.addSemComma(row ['additive2']) +speak.addSemComma(row ['additive3'])+speak.addSemComma(row ['additive4'])\
               +speak.addSemComma(row ['admixtrue1'])  +speak.addSemComma(row ['admixtrue2']) +speak.addSemComma(row ['admixtrue3'])+speak.addSemComma(row ['cement'])\
               +speak.addSemComma(row ['isBig'])  +speak.addSemComma(row ['impervious']) +speak.addSemComma(row ['mixGrade'])+speak.addSemComma(row ['mixId'])\
               +speak.addSemComma(row ['mixPid'])  +speak.addSemComma(row ['sand']) +speak.addSemComma(row ['stone'])+speak.addSemComma(row ['water'])\
               +speak.addSemComma(row ['zmixGrade'])  +speak.addSem(row ['inSpectInstituTionName'])\
               +")"
            speak.executeSQL(st)

'''
def reAllSand():#返回第一页的砂子编号 List形式返回
    rs=speak.reuserName()
    jcjgid=rs.fields.item(2).value
    postData={'reportType':'E05',
              'jcjgId':jcjgid,
              'startSourceDate':netcode.reNday(15),  #'2018-1-15'
              'endSourceDate':netcode.reToday(),
              'curPage':1
    }
    s=post('http://117.27.135.9:8083/sospweb/com/zr/report/reportAction!queryCementReport.do',postData)
    if len(s)<100:
        return "失败，没有查询到任何砂子编号."
    s=s.replace('null','\'null\'')
    print(s)
    di=eval(s)
    di= di['dataList']
    return di

    totalPage=int(di['totalPage'])
    allCompact=[]
    for i in range(1,2):#totalPage+1):
        print('合同编号信息读取第几页：'+str(i))
        s=post('http://117.27.135.9:8083/sospweb/com/zr/report/reportAction!queryCementReport.do',{'curPage':str(i)})
        di=eval(s)
        di=di['dataList']
        #print(di)
        for row in di:
            allCompact.append(row)
    return allCompact


def reMaterial(reportType):#返回第一页的原材料编号 List形式返回
    rs=speak.reuserName()
    jcjgid=rs.fields.item(2).value
    postData={'reportType':reportType,
              'jcjgId':jcjgid,
              'startSourceDate':netcode.reNday(15),  #'2018-1-15'
              'endSourceDate':netcode.reToday(),
              'curPage':1
    }
    print(postData)
    s=post('http://117.27.135.9:8083/sospweb/com/zr/report/reportAction!queryCementReport.do',postData)
    if len(s)<100:
        return "失败，没有查询到任何原材料编号."
    s=s.replace('null','\'null\'')
    print(s)
    di=eval(s)
    di= di['dataList']
    return di
'''
def reMaterialAlways(reportType):#返回第一页的原材料编号 List形式返回 一直找，找到为止。1年为限
    rs=speak.reuserName()
    jcjgid=rs.fields.item(2).value
    allCompact=[]
    for i in range(25):
        j=i*15
        k=j+15-1
        postData={'reportType':reportType,
                  'jcjgId':jcjgid,
                  'startSourceDate':netcode.reNday(k),  #'2018-1-15'
                  'endSourceDate':netcode.reNday(j),
                  'curPage':1
        }
        print(postData)
        s=post('http://117.27.135.9:8083/sospweb/com/zr/report/reportAction!queryCementReport.do',postData)
        if len(s)<100:
            return "失败，没有查询到任何原材料编号."
        else:
            s=s.replace('null','\'null\'')
            #print(s)
            di=eval(s)
            #di= di['dataList']

            totalPage=int(di['totalPage'])

            for i in range(1,totalPage+1):
                print('合同编号信息读取第几页：'+str(i))
                postData['curPage']=str(i)
                s=post('http://117.27.135.9:8083/sospweb/com/zr/report/reportAction!queryCementReport.do',postData)
                #print(s)
                s=s.replace('null','\'null\'')
                di=eval(s)
                di=di['dataList']
                print(di)
                for row in di:
                    allCompact.append(row)
                    #print('长度'+str(len(allCompact)))

        if len(allCompact)>20:
            break
    return allCompact


def pullList(sTemp):  #提交订单！
    #sTemp=netcode.readfile("c:/vb.txt")
    lis=sTemp.split('\n')

    rsUser=speak.reuserName()
    jcjg=rsUser.Fields.item(2).value
    inSpectInstituTionName=rsUser.Fields.item(3).value

    rsProject=speak.executeSQL("select * from 混凝土供应信息 where  主键 like "+speak.addSem(lis[2]))
    rsMixture=speak.executeSQL("select * from 设计配合比信息 where  主键 like "+speak.addSem(lis[3]))
    gkjrwd1=lis[1]
    gkjrwd1=gkjrwd1[len(gkjrwd1)-9:]

    if rsMixture.fields.item(10).value==0:
        impervious='否'
    else:
        impervious='是'

    if rsMixture.fields.item(9).value==0:
        isBig='否'
    else:
        isBig='是'

    print(rsProject.fields.item(1).value)
    print(rsMixture.fields.item(1).value)
    print(gkjrwd1)

    postData = {
    'jcjgId':jcjg,
    'mixPidFlag': "Y",
    'cementFlag': "Y" ,
    'sandFlag':  "Y",
    'stoneFlag':  "Y",
    'additveFlag':  "Y",
    'mixedFlag':  "Y",
    'inSpectInstituTionName': inSpectInstituTionName ,
    'buildUnit':  rsProject.fields.item(1).value,
    'productionTaskId':  lis[1],
    'serializableNum':  rsMixture.fields.item(11).value+"-"+lis[1],
    'gkjrwd1':  gkjrwd1,
    'gkjrwd2':  gkjrwd1,
    'conCreteCompactId':  rsProject.fields.item(3).value,
    'concreteCompactPid': rsProject.fields.item(4).value,
    'conCreteProjectName': rsProject.fields.item(6).value,
    'replacementSite':  lis[4],
    'produceAmount':  lis[5],
    'mixId':  rsMixture.fields.item(12).value,
    'mixPid':rsMixture.fields.item(13).value ,
    'mixGrade':rsMixture.fields.item(11).value,
    'impervious':  impervious,
    'isBig': isBig,
    'zmixGrade': rsMixture.fields.item(17).value,
    'waterWeight': rsMixture.fields.item(16).value,
    'cementWeight': rsMixture.fields.item(8).value,
    'sandWeight': rsMixture.fields.item(14).value,
    'stoneWeight': rsMixture.fields.item(15).value,
    'additve1Weight':  rsMixture.fields.item(1).value,
    'additve2Weight':  rsMixture.fields.item(2).value,
    'additve3Weight':  rsMixture.fields.item(3).value,
    'additve4Weight': rsMixture.fields.item(4).value,
    'admixture1Weight':  rsMixture.fields.item(5).value,
    'admixture2Weight':  rsMixture.fields.item(6).value,
    'admixture3Weight':  rsMixture.fields.item(7).value,
    'sandReportId':  speak.reReportId(lis[6]),
    'sand2ReportId':  speak.reReportId(lis[11]),
    'sand3ReportId': speak.reReportId(lis[16]),
    'stoneReportId': speak.reReportId(lis[7]),
    'stone2ReportId': speak.reReportId(lis[12]),
    'stone3ReportId':  speak.reReportId(lis[17]),
    'cementReportId':  speak.reReportId(lis[8]),
    'mixedReportId': speak.reReportId(lis[13]),
    'slagReportId':speak.reReportId(lis[18]),
    'ashReportId':speak.reReportId(lis[9]),
    'additveOneReportId':speak.reReportId(lis[14]),
    'additveTwoReportId':speak.reReportId(lis[19]),
    'additve3ReportId':speak.reReportId(lis[10]),
    'additve4ReportId':speak.reReportId(lis[15]),
    }
    print(postData)
    spost=post("http://117.27.135.9:8083/sospweb/com/zr/porminrTask/porminrTaskAction!savePorminrTask.do",postData)
    print(spost)
    return spost


