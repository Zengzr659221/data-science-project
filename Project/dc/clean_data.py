import pandas as pd
from geopy.distance import geodesic

class Clean_Data():
   '''
   用来对数据进行处理，包括：
   1、删除不合理的数据、将数据日期转为北京时间、处理经纬度、设置载客状态、
   获取需要的部分字段数据集并按时间排序
   2、提取OD数据
   3、将OD数据进行清理
   '''
   def __init__(self,data):
       self.data=data
       
   def first_clean(self):
       print('正在清理第一步，请等待一段时间......')
       # 删除重复的行和为0的数据
       data = self.data.drop_duplicates(keep='first')  
       data = data.dropna(axis=0, how='any')
       #将时间转为北京时间
       data['time'] = pd.to_datetime(data['UTC'].values, utc=True, unit='s').tz_convert("Asia/Shanghai").to_period("s")
       #维度前两位后加小数点，经度前3位后加小数点，并将字段设置为小写
       data['LAT'] = data['LAT'].astype(str)
       data['lat'] = data['LAT'].apply(lambda x: float(x[:2]+'.'+x[2:]))
       data['LON'] = data['LON'].astype(str)
       data['lng'] = data['LON'].apply(lambda x: float(x[:3]+'.'+x[3:]))
       
       #设置载客状态
       data_flag = list(dict(data['TFLAG'].value_counts()).keys())      # 所有的flag的标签
       # 268435456设置为1，表示载客；其余均为空客状态，设置为0
       flag_dict = {}
       for k in data_flag:
           if k == 268435456:
               flag_dict[k] = 1
           else:
               flag_dict[k] = 0
       # 替换flag标签的表示方式，只设置为载客与空客两种状态
       data['FLAG'] = data['TFLAG'].replace(flag_dict)
       
       # 新的数据集，[车牌号，时间，纬度，经度，方向角，速度，载客/空客]
       data_new = data[['COMMADDR', 'time', 'lat', 'lng', 'HEAD', 'SPEED', 'FLAG','UTC']]
       data_new.set_index('time', inplace=True)    # 时间列设置为索引  
       data_new=data_new.sort_index()   # 索引是时间，按照时间排序
       data_new=data_new.reset_index()
       return data_new

   def od(self):
       print('正在提取od数据，请等待一段时间......')
       data_new=self.data.drop('UTC',axis=1)        
       '根据车牌号分组，提取OD数据'
       groups = data_new.groupby('COMMADDR')
       OD = []
       for name, group in groups:
           data0 = group      # 提取车牌对应的轨迹数据
           data0 = data0.sort_values('time')     # 按照时间排序
           data0['od_flag'] = data0['FLAG'].diff()     # '1'表示上客点O，'-1'表示下客点D
           data_od = data0[(data0['od_flag'] == 1) | (data0['od_flag'] == -1)]      # 提取上客点与下客点的数据
           # 上下客点的数量要大于等于2
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
       return result
   
   def od_clean(self):
       
       print('正在清理od数据，请等待一段时间......')
       
       #删除不合理的数据
       data_drop = self.data.drop_duplicates(keep='first')       # 删除重复的行
       data = data_drop.dropna(axis=0, how='any')      # 删除空值的行      
       data['O_COMMADDR']=data['O_COMMADDR'].apply(lambda x:str(x))
       data['D_COMMADDR']=data['D_COMMADDR'].apply(lambda x:str(x))
       #删除不合理的OD时间
       data['OD_TIME_s'] =(pd.to_timedelta(data['D_time'] - data['O_time']))
       #转换为秒的整数
       data['OD_TIME_s']=data['OD_TIME_s'].apply(lambda x:int(x.total_seconds()))
       data = data[(data['OD_TIME_s'] > 3*60) & (data['OD_TIME_s'] < 2*60*60)]      # 选择大于三分钟小于两小时的OD对
       
       #删除不合理的OD距离
       # 济南的经纬度，经度:116.98 纬度:36.67      116.98, 36.67
       data = data[(data['O_lat'] > 30) & (data['O_lat'] < 40)]
       data = data[(data['O_lng'] > 110) & (data['O_lng'] < 125)]
       data = data[(data['D_lat'] > 30) & (data['D_lat'] < 40)]
       data = data[(data['D_lng'] > 110) & (data['D_lng'] < 125)]
       data['OD_Dis_km'] = data.apply(lambda x: geodesic((x['O_lat'], x['O_lng']), (x['D_lat'], x['D_lng'])).km, axis=1)
       
       # data.columns
       data = data[['O_COMMADDR', 'O_time', 'O_lat', 'O_lng', 'O_HEAD', 'O_SPEED', 'O_FLAG', 'D_time', 'D_lat', 'D_lng',
                    'D_HEAD', 'D_SPEED', 'D_FLAG', 'OD_TIME_s', 'OD_Dis_km']]
       return data