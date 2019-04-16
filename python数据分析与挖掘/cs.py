import pandas as pd
import numpy as np

#规范化、归一化----------------------------------------------------------------

datafile = './data-analysis-master/data_preprocess/data/normalization_data.xls'

data = pd.read_excel(datafile,header = None)  #读取数据

print((data - data.min())/(data.max() - data.min()))     #最小减最大规范化
print((data - data.mean())/data.std())    #零均值规范化
print(data/10**np.ceil(np.log10(data.abs().max())))       #小数定标规范化

#-----------------------------------------------------------------------------
datafile = './data-analysis-master/data_preprocess/data/discretization_data.xls'        #参数初始化

data = pd.read_excel(datafile)
data = data[u'肝气郁结证型系数'].copy()
k=4

d1 = pd.cut(data,k,labels = range(k))   #等宽度离散化，各个类比以此命名为0，1，2，3

#等频率离散化
w = [1.0*i/k for i in range(k+1)]
w = data.describe(percentiles = w)[4:4+k+1]     #使用describe函数自动计算分位数
w[0] = w[0]*(1-1e-10)
d2 = pd.cut(data,w,labels = range(k))

from sklearn.cluster import KMeans
kmodel = KMeans(n_clusters = k,n_jobs= 4)    #建立模型， n_jobs是并行数，一般等于CPU数较好
# kmodel.fit(data.reshape((len(data),1)))     #训练模型
# c = pd.DataFrame(kmodel.cluster_centers_).sort(0)   #输出是聚类心中，并且排序（默认是随机序的）
# w = pd.rolling_mean(c,2).iloc[1:]   #相邻两项求中点，作为边界点
# w = [0] +list(w[0]) + [data.max()]  #把首末边界点加上
# d3 = pd.cut(data,w,labels= range(k))

def cluster_plot(d,k):  #自定义作图函数来显示聚类结果
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号

    plt.figure(figsize=(8, 3))
    for j in range(0, k):
        plt.plot(data[d==j], [j for i in d[d==j]], 'o')

    plt.ylim(-0.5, k-0.5)
    return plt

cluster_plot(d1, k).show()
cluster_plot(d2, k).show()
# cluster_plot(d3, k).show()

#--------------------------------------------------------------------------------------
#利用小波进行分析特征分析

#参数初始化
inputfile = './data-analysis-master/data_preprocess/data/leleccum.mat'  #提取自Matlab的信号文件

from scipy.io import loadmat     #mat是python的专用格式，需要用loadmat读取它
mat = loadmat(inputfile)
signal = mat['leleccum'][0]

import pywt     #导入PyWavelets
coeffs =pywt.wavedec(signal,'bior3.7',leval = 5)






