import pandas as pd
import numpy as np
x_pi = np.pi * 3000.0 / 180.0
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323 # 扁率
def gcj02_to_bd09(lng,lat):
   """
   火星坐标系(GCJ-02)转百度坐标系(BD-09)
   谷歌、高德——>百度
   :param data:火星坐标经度的数据dataframe
   :return:
   """
   z = np.sqrt(lng * lng + lat * lat) + 0.00002 * np.sin(lat * x_pi)
   theta = np.arctan2(lat, lng) + 0.000003 * np.cos(lng * x_pi)
   bd_lng = z * np.cos(theta) + 0.0065
   bd_lat = z * np.sin(theta) + 0.006
   return [bd_lng, bd_lat]
def wgs84_to_gcj02(lng,lat):
   """
   WGS84转GCJ02(火星坐标系)
   :param lng:WGS84坐标系的经度
   :param lat:WGS84坐标系的纬度
   :return:
   """
   dlat = transform_lat(lng - 105, lat - 35)
   dlng = transform_lng(lng - 105, lat - 35)
   radlat = lat / 180* np.pi
   magic = np.sin(radlat)
   magic = 1 - ee * magic * magic
   sqrtmagic = np.sqrt(magic)
   dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * np.pi)
   dlng = (dlng * 180.0) / (a / sqrtmagic * np.cos(radlat) * np.pi)
   mglat = lat + dlat
   mglng = lng + dlng
   return [mglng, mglat]

def wgs84_to_bd09(lon, lat):
   lon, lat = wgs84_to_gcj02(lon, lat)
   return gcj02_to_bd09(lon, lat)

#纬度转换
def transform_lat(lng,lat):
   ret=-100+2*lng+3*lat+0.2*(lat**2)+0.1*lng*lat+0.2*np.sqrt(np.abs(lng))
   ret+=(20*np.sin(6*lng*np.pi)+20*np.sin(2*lng*np.pi))*2/3
   ret+=(20*np.sin(lat*np.pi)+40*np.sin(lat/3*np.pi))*2/3
   ret+=(160*np.sin(lat/12*np.pi)+320*np.sin(lat*np.pi/30))*2/3
   return ret
#经度转换
def transform_lng(lng,lat):
   ret=300+lng+2*lat+0.1*(lng**2)+0.1*lng*lat+0.1*np.sqrt(np.abs(lng))
   ret+=(20*np.sin(6*lng*np.pi)+20*np.sin(2*lng*np.pi))*2/3
   ret+=(20*np.sin(lng*np.pi)+40*np.sin(lng/3*np.pi))*2/3
   ret+=(150*np.sin(lng/12*np.pi)+300*np.sin(lng/30*np.pi))*2/3
   return ret

if __name__ == '__main__':
   mydata = pd.read_csv('data/0912_temp.csv')
   mydata=mydata.iloc[:,1:]
   print(mydata.head())
   # 原坐标系为84坐标系，现转为百度
   mydata['lat']=wgs84_to_bd09(mydata['lng'],mydata['lat'])[1]
   mydata['lng']=wgs84_to_bd09(mydata['lng'],mydata['lat'])[0]
   mydata.to_csv('data/0912_view.csv', sep=',', encoding='utf_8_sig', header=True, index=False)