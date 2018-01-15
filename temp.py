##coding:utf-8
#python 3版本  这个模块用于连接数据库
import netcode
import pypyodbc,os

'''
 On Error GoTo ExecuteSQL_Error
   sTokens = Split(SQL)  '这个函数可以把单词分开来
   If InStr("INSERT,DELETE,UPDATE", UCase$(sTokens(0))) Then  '如果以这3个单词开头，则。。。。
      CNN.Execute SQL
   Else
      Set Rst = New ADODB.Recordset
      CNN.CursorLocation = adUseClient  '启用客户游标，让datagrid1显示
      Rst.Open Trim$(SQL), CNN, adOpenKeyset, adLockOptimistic
      Set ExecuteSQL = Rst
   End If
'''
#实例化数据库引擎
import win32com.client
conn = win32com.client.Dispatch(r'ADODB.Connection')
DSN = 'PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=D:/XW/python/business/py/db1.mdb;'
conn.Open(DSN)
rs = win32com.client.Dispatch(r'ADODB.Recordset')

def executeSQL(sSQL):
    st=sSQL.split()[0].lower()
    if st=='insert' or st=='delete' or st=='update':
        rs.Open(sSQL, conn, 1, 3)
    else:
        rs.CursorLocation = 3
        rs.Open(sSQL, conn, 1, 3)
        return rs


#rs.Open("UPDATE communi SET a='你好' WHERE 主键=1;", conn, 1, 3)
#rs.Open("select * from  communi;", conn, 1, 3)
#data=rs.GetRows()

#rs.Open('Select * FROM communi', conn)


#print(data)
#conn.Close()
rs=executeSQL('Select * from 混凝土供应信息')
print(rs.Fields.item(3).Value)
rs.MoveNext()
print(rs.Fields.item(3).Value)
print(rs)

#rs.CursorLocation = 3
#rs.Open('Select * from 混凝土供应信息', conn, 1, 3)
#print(rs.Fields.Item(1).Value)