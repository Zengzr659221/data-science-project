import pandas as pd
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import math
import numpy as np
import datetime

def dist(a, b):      # 计算欧几里得距离,a,b分别为两个元组
   return math.sqrt(math.pow(a[0]-b[0], 2) + math.pow(a[1]-b[1], 2))

def center(D):
   wdsum = 0
   jdsum = 0
   cen = []
   for q in range(len(D)):    # 遍历D, D是簇的集合
       dis = []  # 存放簇中点到中心点的距离
       for s in range(len(D[q])):    # 遍历一个簇中每个点
           wdsum = wdsum + D[q][s][0]  # 簇中点经度，纬度求和
           jdsum = jdsum + D[q][s][1]
       K = (wdsum / len(D[q]), jdsum / len(D[q]))  # 簇中心点
       wdsum = 0  # D簇的集合，D[0]单个簇，D[0][0]单个簇中的一个点的经纬度坐标
       jdsum = 0  # D[0][0][0]单个簇中的一个点的经度坐标1或纬度坐标0
       for ss in range(len(D[q])):
           dis.append(dist(K, D[q][ss]))
       cen.append(list(D[q][dis.index(min(dis))])+[len(D[q])])  # 存放距离中心点最近的簇中点坐标，以及簇中点的数量
   return cen

data = pd.read_csv('0912_od_wh_drop.csv', dtype={'O_COMMADDR': str})
print(data.head())

data = data[['O_time', 'O_lat', 'O_lng']]
data = data.sort_values('O_time')
data['O_time'] = pd.to_datetime(data['O_time'], format='%Y-%m-%d %H:%M:%S')
data = data.set_index('O_time')
print(data.head())

data_series = pd.period_range("2013-09-12", "2013-09-13", freq="15min").tolist()      # 15分钟等间隔划分时间序列
print(data_series)

ALL = []
for ser in range(len(data_series)-1):      # 遍历每一个时间段
   print(str(data_series[ser]))
   if data_series[ser].hour > 7:
       min_sample = 5
   else:
       min_sample = 3
   # 提取时间间隔内的上客点数据
   data_0 = data[str(data_series[ser]):str(data_series[ser+1]-datetime.timedelta(minutes=1))]     
   # 数据按照序列号聚类，这里只针对车辆数据.csv
   lat = data_0.O_lat.tolist()             # 数据的索引作为list列表
   lng = data_0.O_lng.tolist()
   X = list(zip(lat, lng))                 # 组成二维列表用于后面的聚类
   y_pred = DBSCAN(eps=0.0005, min_samples=min_sample).fit_predict(X)   # DBSCAN聚类, 1度=111110m, 0.001差不多代表110米左右
   print(max(y_pred))
   
   # 对序列号聚类画出结果图，可以看出紫色开始，黄色结束，列出前3个图
   if ser<3:
       plt.figure()
       plt.scatter(lat[:], lng[:], linewidths=0, c=y_pred)        
       plt.xlim(36.6, 36.74)
       plt.ylim(116.8, 117.3)
       plt.show()
   # 查找聚类后每一类里面的元素
   dict_address = {}
   for i in list(set(y_pred.tolist())):   # 遍历聚类结果，聚类结果是0到12（或更大）的聚类成每一组的序号，离散点表示为-1
       if i != -1:     # 离散点-1，不需要关心
           address_index = [X[x] for x in range(len(y_pred.tolist())) if y_pred.tolist()[x] == i]
           dict_address[i] = address_index     # 转化为字典形式，i为聚类的后的组号，address_index为聚类后i包含的坐标点
   # 判断每一簇的中心点，以及簇中点的数量
   cen = center(list(dict_address.values()))   # cen -> [维度，经度，簇的点集数量]
   cen = np.array(cen)       # list转为数组
   cen = pd.DataFrame(cen)   # 数组转为DataFrame
   cen.columns = ['lat', 'lng', 'count']    # [纬度，经度，数量]
   cen['time'] = [str(data_series[ser])]*len(cen)
   ALL.append(cen)
   
result = pd.concat(ALL, ignore_index=True)
print(result)

result.to_csv(r'0912_heart.csv', sep=',', encoding='utf_8_sig', header=True, index=False)