#coding:utf-8
#python 3  这个模块用于跟网站沟通
import datetime,time,os

import urllib,speak
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
    user=speak.reuserName()
    username = user[0][0]
    password = user[0][1]
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
        s=speak.reuserName()
        jcjg=str(s[0][2])
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

def returnOpener():
    cookie = returnCookie()
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = build_opener(handler)
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



def returnStartTime():
    #返回起始时间，用于向服务器请求数据
    if datetime.datetime.now().hour>8:
        return  time.strftime('%Y-%m-%d',time.localtime(time.time()))
    else:
        t= datetime.datetime.now() + datetime.timedelta(days=-1)
        s=str(t.year)+'-'+str(t.month)+'-'+str(t.day)
        return s
'''
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
    s=speak.reuserName()
    jcjg=str(s[0][2])
    s=post('http://117.27.135.9:8083/sospweb/com/zr/porminrTask/porminrTaskAction!getProductionTaskId.do',{'jcjgId':jcjg})
    s=s.replace('true','\'true\'')
    di=eval(s)
    return di['message']
#print(rePlatformSerialNnumber())

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
def reAllAllHntMix():#返回所有的配合比信息 List形式返回
    s=post('http://117.27.135.9:8083/sospweb/com/zr/hntmix/hntmixAction!queryAllHntMix.do',{'curPage':'1'})
    if len(s)<100:
        return "失败，没有查询到任何配合比信息."
    #print(s)
    #s=s.replace('true','\'true\'')
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
              admixtrue1,admixtrue2,admixtrue3,cement,isBig,isInsert,mixGrade,mixId,mixPid,sand,stone,water,zmixGrade,inSpectInstituTionName) VALUES ("\
               +speak.addSemComma(row ['additive1'])  +speak.addSemComma(row ['additive2']) +speak.addSemComma(row ['additive3'])+speak.addSemComma(row ['additive4'])\
               +speak.addSemComma(row ['admixtrue1'])  +speak.addSemComma(row ['admixtrue2']) +speak.addSemComma(row ['admixtrue3'])+speak.addSemComma(row ['cement'])\
               +speak.addSemComma(row ['isBig'])  +speak.addSemComma(row ['isInsert']) +speak.addSemComma(row ['mixGrade'])+speak.addSemComma(row ['mixId'])\
               +speak.addSemComma(row ['mixPid'])  +speak.addSemComma(row ['sand']) +speak.addSemComma(row ['stone'])+speak.addSemComma(row ['water'])\
               +speak.addSemComma(row ['zmixGrade'])  +speak.addSem(row ['inSpectInstituTionName'])\
               +")"
            speak.cur.execute(st)
        speak.cur.commit()
    return allMix

#print(rePlatformSerialNnumber())

