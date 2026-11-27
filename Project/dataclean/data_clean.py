import pandas as pd

data =pd.read_csv(r'data\jn0912.csv')
print(data.info())

data = data.drop_duplicates(keep='first')

data = data.dropna(axis=0, how='any')

data0 = data[data['COMMADDR'] == 15053119982]    # 提取一辆车一天内的轨迹
data0 = data0.sort_values('UTC')
print(data0['UTC'].diff())            # 采样间隔为15秒

print(data['HEAD'].max(), data['HEAD'].min())

print(data['TFLAG'].value_counts())

print(data['SPEED'].max(), data['SPEED'].min())

print(data.head())

# UTC时间转变为北京时间
data['time'] = pd.to_datetime(data['UTC'].values, utc=True, unit='s').tz_convert("Asia/Shanghai").to_period("s")
data['LAT'] = data['LAT'].astype(str)         # 纬度保留前两位为整数
data['lat'] = data['LAT'].apply(lambda x: float(x[:2]+'.'+x[2:]))
data['LON'] = data['LON'].astype(str)         # 经度保留前三位为整数
data['lng'] = data['LON'].apply(lambda x: float(x[:3]+'.'+x[3:]))
print(data.head())

data_flag = list(dict(data['TFLAG'].value_counts()).keys())      # 所有的flag的标签
print(data_flag)

flag_dict = {}
for k in data_flag:
    if k == 268435456:
        flag_dict[k] = 1
    else:
        flag_dict[k] = 0
print(flag_dict)       # 替换flag标签的表示方式，只设置为载客与空客两种状态

data['FLAG'] = data['TFLAG'].replace(flag_dict)
print(data['FLAG'].value_counts())

# 新的数据集，[车牌号，时间，纬度，经度，方向角，速度，载客/空客]
data_new = data[['COMMADDR', 'time', 'lat', 'lng', 'HEAD', 'SPEED', 'FLAG','UTC']]
data_new.set_index('time', inplace=True)    # 时间列设置为索引
print(data_new.head())

groups = data_new.groupby('COMMADDR')
print(groups.size())         # 根据车牌号分组

data0 = data_new[data_new['COMMADDR'] == 15053119982]   # 提取一辆车一天内的轨迹
data0 = data0.sort_index()    # 索引是时间，按照时间排序
print(data0.head())

data_new=data_new.sort_index()   # 索引是时间，按照时间排序
data_new.to_csv(r'0912.csv', sep=',', encoding='utf_8_sig', header=True, index=True)
data_new1=data_new[['COMMADDR','UTC','lat','lng']]
data_new1=data_new1.rename(columns={'COMMADDR':'CarId'})
data_new1=data_new1.sort_values(['CarId','UTC'])
data_new1.to_csv(r'0912_temp.csv', sep=',', encoding='utf_8_sig', header=True, index=True)