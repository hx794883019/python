# -*- coding: utf-8 -*-
from __future__ import print_function   #兼容

import pandas as pd
catering_sale = './data-analysis-master/data_exploratory/data/catering_sale.xls'
data = pd.read_excel(catering_sale, index_col = u'日期')            #读取数据，指定“日期”列为索引列
print(data.describe())
print(len(data))

# ----------------------------------------------------------------------------------------------------------------

#筛选异常数据
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']     #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False       #用来正常显示负号

plt.figure()    #建立图像
p = data.boxplot(return_type='dict')      #画箱线图
x = p['fliers'][0].get_xdata()      #'fliers'即为异常值标签
y = p['fliers'][0].get_ydata()
y.sort()        #从小到大排序，该方法直接改变原对象

#用annotate添加注释
for i in range(len(x)):
    if i>0:
        plt.annotate(y[i], xy = (x[i], y[i]), xytext=(x[i]+0.05-0.8/(y[i]-y[i-1]),y[i]))
    else:
        plt.annotate(y[i], xy = (x[i],y[i]), xytext=(x[i]+0.08,y[i]))

plt.show()     #展示箱线图

# -------------------------------------------------------------------------------------------------------------

# 帕累托图
import pandas as pd

dish_profit = './data-analysis-master/data_exploratory/data/catering_dish_profit.xls'
data = pd.read_excel(dish_profit,index_col = u'菜品名')
data = data[u'盈利'].copy()
data.sort_values(ascending = False)

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']     #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False       #用来正常显示负号

plt.figure()
data.plot(kind = 'bar')     #柱状图
plt.ylabel(u'盈利(元)')

p = 1.0*data.cumsum()/data.sum()
p.plot(color = 'r',secondary_y = True,style = '-o',linewidth = 2)      #线
#添加注释，即85%处的标记。这里包括了指示箭头样式
plt.annotate(format(p[6],'.4%'),\
             xy = (6,p[6]),\
             xytext = (6*0.9,p[6]*0.9),\
             arrowprops = dict(arrowstyle = "->", connectionstyle = "arc3,rad=.2"))

plt.ylabel(u'盈利(比例)')
plt.show()

#------------------------------------------------------------------------------------------------------------
import pandas as pd

catering_sale_all = './data-analysis-master/data_exploratory/data/catering_sale_all.xls'
data = pd.read_excel(catering_sale_all,index_col=u'日期')

print(data.corr())         #相关系数矩阵，即给出任意两款菜式之间的相关系数
#print(data.corr())
print(data.corr()[u'百合酱蒸凤爪']) #只显示“百合酱蒸凤爪”与其他菜式的相关系数
print('\n')
print(data[u'百合酱蒸凤爪'].corr(data[u'翡翠蒸香茜饺'])) #计算“百合酱蒸凤爪”与“翡翠蒸香茜饺”的相关系数



#------------------------------------------------------------------------------------------------------------
import pandas as pd
from scipy.interpolate import lagrange  #导入拉格朗日插值函数

inputfile = './data-analysis-master/data_exploratory/data/catering_sale.xls'        #输入数据路径
outputfile = './tmp/sales.xls'  #输出数据路径

data = pd.read_excel(inputfile)  #读入数据
data.loc[(data[u'销量'] < 400) | (data[u'销量'] > 5000),u'销量'] = None  #过滤异常值，将其变为空值

#自定义列向量插值函数
#s为列向量，n为被插值的位置，k为取前后的数据个数，默认为5
def ployinterp_column(s, n, k=5):
    y = s[list(range(n-k, n))+list(range(n+1,n+1+k))]       #取数
    y = y[y.notnull()]  #剔除空值
    return lagrange(y.index, list(y))(n)    #插值并返回插值结束

#逐个元素判断是否需要插值
for i in data.columns:
    for j in range(len(data)):
        if (data[i].isnull())[j]:        #如果为空即为插值
            data.loc[[i],[j]] = ployinterp_column(data[i], j)

data.to_excel(outputfile)   #输出结果，写入文件

#---------------------------------------------------------------------------------------------------------------------

datafile = './data-analysis-master/data_preprocess/data/normalization_data.xls'

data = pd.read_excel(datafile,header = None)  #读取数据

print((data - data.min())/(data.max() - data.min()))     #最小减最大规范化
(data - data.mean())/data.std()     #零均值规范化
data/10**np.ceil(np.log10(data.abs().max()))    #小数定标规范化