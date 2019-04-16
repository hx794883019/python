'''
import re
a='booooooooooobbo'
pat='.*b'
b=re.compile(pat).findall(a)
print(b)
'''

import pymysql
import pandas as pd
conn=pymysql.connect(host='localhost',user='root',passwd='huangxu',db='scrapySpider')
sql='select * from article'
k=pd.read_sql(sql,conn)
print(k)