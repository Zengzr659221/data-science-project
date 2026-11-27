import pandas as pd
from geopy.distance import geodesic

data_new=pd.read_csv('data/0912.csv')
data_new=data_new.drop('UTC',axis=1)
print(data_new.info())

groups = data_new.groupby('COMMADDR')
print(groups.size())         # 根据车牌号分组

OD = []
for name, group in groups:
   print(name)        # 打印车牌
   data0 = group      # 提取车牌对应的轨迹数据
   data0 = data0.sort_values('time')     # 按照时间排序
   data0['od_flag'] = data0['FLAG'].diff()     # '1'表示上客点O，'-1'表示下客点D
   data_od = data0[(data0['od_flag'] == 1) | (data0['od_flag'] == -1)]      # 提取上客点与下客点的数据
   print(len(data_od))      # 上下客点的数量要大于等于2
   if len(data_od) > 1:
       # 保证上客'1'打头，下客'-1'结尾
       data_od.index = range(len(data_od))      # 重新设置索引
       if data_od['od_flag'].tolist()[0] == -1:     # 如果开头的不是1而是-1.删除第一行
           data_od = data_od.drop([0])
       if data_od['od_flag'].tolist()[-1] == 1:      # 如果结尾的不是-1而是1.删除最后一行
           data_od = data_od.drop([data_od.index[-1]])
       # 分开上客点与下客点，进行横向合并
       data_o = data_od[(data_od['od_flag'] == 1)]      # 提取上客点的数据
       data_o.index = range(len(data_o))
       data_o.columns = ['O_time','O_COMMADDR', 'O_lat', 'O_lng', 'O_HEAD', 'O_SPEED', 'O_FLAG','O_od_flag']
       data_d = data_od[(data_od['od_flag'] == -1)]     # 提取下客点的数据
       data_d.index = range(len(data_d))
       data_d.columns = ['D_time','D_COMMADDR', 'D_lat', 'D_lng', 'D_HEAD', 'D_SPEED', 'D_FLAG','D_od_flag']
       result_od = pd.concat([data_o, data_d], axis=1)     # 横向合并
       OD.append(result_od)
result = pd.concat(OD)
result.index = range(len(result))
print(result.info())

#将车号转为string类型
data = result.copy()
data['O_COMMADDR']=data['O_COMMADDR'].apply(lambda x:str(x))
data['D_COMMADDR']=data['D_COMMADDR'].apply(lambda x:str(x))
print(data.info())

data_drop = data.drop_duplicates(keep='first')       # 删除重复的行
data = data_drop.dropna(axis=0, how='any')      # 删除空值的行
print(data['O_FLAG'].value_counts())

data['O_time'] = pd.to_datetime(data['O_time'], format='%Y-%m-%d %H:%M:%S')
data['D_time'] = pd.to_datetime(data['D_time'], format='%Y-%m-%d %H:%M:%S')
data['OD_TIME'] = data['D_time'] - data['O_time']
data['OD_TIME_s'] = data.apply(lambda x: x['OD_TIME'].total_seconds(), axis=1)        # 将时间差转换为秒为单位
print(data['OD_TIME_s'].min())

data = data[(data['OD_TIME_s'] > 3*60) & (data['OD_TIME_s'] < 2*60*60)]      # 选择大于三分钟小于两小时的OD对
print(data.info())

# 济南的经纬度，经度:116.98 纬度:36.67
data = data[(data['O_lat'] > 30) & (data['O_lat'] < 40)]
data = data[(data['O_lng'] > 110) & (data['O_lng'] < 125)]
data = data[(data['D_lat'] > 30) & (data['D_lat'] < 40)]
data = data[(data['D_lng'] > 110) & (data['D_lng'] < 125)]
print(data.info())

data['OD_Dis_km'] = data.apply(lambda x: geodesic((x['O_lat'], x['O_lng']), (x['D_lat'], x['D_lng'])).km, axis=1)
print(data['OD_Dis_km'].min(), data['OD_Dis_km'].max())

data = data[['O_COMMADDR', 'O_time', 'O_lat', 'O_lng', 'O_HEAD', 'O_SPEED', 'O_FLAG', 'D_time', 'D_lat', 'D_lng',
            'D_HEAD', 'D_SPEED', 'D_FLAG', 'OD_TIME_s', 'OD_Dis_km']]
data.to_csv('data/0912_od_wh_drop.csv', sep=',', encoding='utf_8_sig', header=True, index=False)