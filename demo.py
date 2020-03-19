# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
import os
from quantactic import backtest,sql_connector,mylog,MyThread,DBupdate,DBcheck,DBtransplant

user1 = 'ReadUser'
user2 = 'root'
pw1 = 'MingHong@601'
pw2 = '7026155@Liu'
h1 = '10.1.10.205'
h2 = '127.0.0.1'
p = 3306
sch1 = 'wind'
sch2 = 'astocks'
#output_engine = sql_connector(user1,pw1,h1,p,sch1)
input_engine = sql_connector(user2,pw2,h2,p,sch2)
obj_engine = input_engine

username,password,server,port,schema = 'root','7026155@Liu','127.0.0.1',3306,'astocks'

'''DEMO 1 backtest '''
start = 20080101
end = 20180631
engine = input_engine
query = "select * from indexweight where codenum='000905.SH' and td>"+str(start)+' and td<'+str(end)+';'
data = pd.read_sql(query,input_engine)
'''you should guarentee that there is no Duplicated and None values'''
data.dropna(inplace=True)
data.drop_duplicates(inplace=True)
'''weight format:
-----+---------+---------+---------+------+---
date | code 1  |  code 2 |  code 3 | .... |   
-----+---------+---------+---------+------+---
  t1 |weight 11|weight 21|weight 31|......|
-----+---------+---------+---------+------+---
*date format:int or string'''
weight = data.pivot(index='td',columns='code',values='weight')
'''when your data show some unnesscary blank space you should remove this by SQL syntax 'replace'.'''
backtest(weight,start,end,input_engine,benchmark='000905.SH')
'''DEMO 2 DBupdate'''
DBupdate('IF',output_engine,input_engine)
'''DEMO 3 DBcheck'''
DBcheck('Ma',output_engine,input_engine)
'''DEMO 4 DBDBtransplant'''
filepath = 'F:\\astocks'
DBtransplant(input_engine,filepath,"in")

import pandas as pd
import numpy as np
df=pd.read_csv('G:\\351.csv',index_col=0,parse_dates=True)
df351=df/1000
xdf = pd.read_excel('G:\\xret.xlsx',index_col=0,parse_dates=True)
df1300 = pd.read_csv('G:\\top1300_ret.csv',index_col=0,parse_dates=True)
df1300=df1300.reindex(df351.index)
xdf = xdf.sort_index().fillna(method='ffill')
xret = xdf['PX_LAST'].pct_change()
df351.insert(0,'PX',xret)
df351.insert(0,'top1300',df1300)
df351.dropna(inplace=True)
allnet=np.cumprod(df351+1,axis=0)
import statsmodels.api as sm
mod=sm.OLS(allnet['PX'],sm.add_constant(allnet[['000300.SH','top1300']])).fit()
allnet.insert(0,'new',pd.DataFrame(mod.predict(),index=allnet.index))



