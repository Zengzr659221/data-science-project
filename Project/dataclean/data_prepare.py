import numpy as np
import pandas as pd
from dc.clean_data import *
from dc.def_func import *
import warnings
warnings.filterwarnings('ignore')    #忽略警告

JN_TIME_O=pd.DataFrame()
JN_TIME_O_WEEK=pd.DataFrame()
record=pd.DataFrame()
JN_5T_kmh=pd.DataFrame()
JN_o_number=pd.DataFrame()
JN_LuC=pd.DataFrame()

for i in range(2,9):
   
   #读取数据
   csv_path='jn091%d.csv'%i
   print('正在读取%s的数据，请等候片刻'%csv_path)
   mydata=pd.read_csv(csv_path)
   
    #清理数据
   print('正在清理%s的数据，请等候片刻'%csv_path)
   #、删除不合理的数据、将数据日期转为北京时间、处理经纬度、设置载客状态、
   #获取需要的部分字段数据集并按时间排序
   cd=Clean_Data(mydata)
   mydata=cd.first_clean()
   
    # 提取OD数据   
   cd=Clean_Data(mydata)
   mydata=cd.od()
   
    # 将OD数据进行清理
   cd=Clean_Data(mydata)
   mydata=cd.od_clean()
   print('清理完成，继续后面的步骤')
   
    #将O_time时间转为string类型
   mydata['O_time']=mydata['O_time'].apply(lambda x:str(x))
   
   #将数据按照15分钟进行划分，并聚合汇总出各时间段车辆数量
   print('正在将数据按照15分钟进行划分，并聚合汇总出各时间段车辆数量')
   mydata['O_time1']=mydata['O_time'].apply(lambda x:x[:14]+catgory_min(x[14:16])+':00')
   # 修改：双层括号返回DataFrame，避免后续Series[:,0]报错
   data_group=mydata.groupby(['O_time1'])[['O_time1']].count()    
   JN_TIME_O=pd.concat([JN_TIME_O,data_group],axis=0)
   
   #将数据按照整点划分，并聚合汇总出各整点的车辆数量
   print('正在将数据按照整点划分，并聚合汇总出各整点的车辆数量')
   mydata['O_time2']=mydata['O_time'].apply(lambda x:x[:14]+'00:00')
   # 修改：双层括号返回DataFrame
   data_group1=mydata.groupby(['O_time2'])[['O_time2']].count()
   JN_TIME_O_WEEK=pd.concat([JN_TIME_O_WEEK,data_group1],axis=0)
   
    #根据OD订单的的数据，提取出[距离、时段和耗时]的json数据
   print('正在根据OD订单的的数据，提取出[距离、时段和耗时]的json数据')
   mydata['O_time3']=mydata['O_time2'].apply(lambda x:int(x[11:13]))
   #将距离的千米转换为米,并保留0位小数
   mydata['OD_Dis_m']=round(mydata['OD_Dis_km']*1000,0)
   newdata=mydata[['OD_Dis_m','O_time3','OD_TIME_s']]
   record=pd.concat([record,newdata],axis=0)
   
    #以5分钟为时间间隔统计每个时间段内，城市道路速度的平均值
   #将数据按照5分钟进行划分，并聚合汇总出各时间段的距离和时间总和
   print('正在将数据按照5分钟进行划分，并聚合汇总出各时间段的距离和时间总和')
   mydata['O_time4']=mydata['O_time'].apply(lambda x:x[:14]+catgory_min1(x[14:16])+':00')
   # ✅修复原报错：多列使用双层方括号
   speed_group=mydata.groupby(['O_time4'])[['OD_TIME_s','OD_Dis_km']].sum()
   JN_5T_kmh=pd.concat([JN_5T_kmh,speed_group],axis=0)
   
    #将OD数据以1分钟的时间间隔进行采样，统计载客出租车的数量
   print('正在将OD数据以1分钟的时间间隔进行采样，统计载客出租车的数量')
   mydata['O_time5']=mydata['O_time'].apply(lambda x:x[:16]+':00')
   # 修改：双层括号返回DataFrame
   num_group=mydata.groupby(['O_time5'])[['O_time5']].count()    
   JN_o_number=pd.concat([JN_o_number,num_group],axis=0)
   
    #根据OD订单的路程，并以4千与8千米为阈值划分出行订单的短途、中途、长途三种出行距离。
   #将OD数据以每天时间间隔统计出短中长途的载客出租车数量
   print('正在将OD数据以每天时间间隔统计出短中长途的载客出租车数量')
   mydata['day']=i-1
   mydata['distance']=mydata['OD_Dis_km'].apply(lambda x:catgory_dis(x))
   ds_data=mydata[['day','distance']]
   JN_LuC=pd.concat([JN_LuC,ds_data],axis=0)
   
#JN_TIME_O.csv
time_o_df=pd.DataFrame({'O_time':JN_TIME_O.index,'count':JN_TIME_O.values[:,0]})
time_o_df.to_csv('JN_TIME_O.csv',index=False,encoding='utf_8_sig')
#JN_TIME_O_WEEK.csv
week_time_df=pd.DataFrame({'time':JN_TIME_O_WEEK.index,'count':JN_TIME_O_WEEK.values[:,0]})
week_time_df.to_csv('JN_TIME_O_WEEK.csv',index=False,encoding='utf_8_sig')
#record.json
record.to_json('record.json',orient='values')
#JN_5T_kmh.csv
JN_5T_kmh['sudu']=JN_5T_kmh['OD_Dis_km']/(JN_5T_kmh['OD_TIME_s']/3600)
JN_5T_kmh=JN_5T_kmh.drop(['OD_TIME_s','OD_Dis_km'],axis=1)
JN_5T_kmh=JN_5T_kmh.reset_index()
JN_5T_kmh.columns=['O_time','sudu']
JN_5T_kmh.to_csv('JN_5T_kmh.csv',index=False,encoding='utf_8_sig')
#JN_o_number.csv
num_time_df=pd.DataFrame({'O_time':JN_o_number.index,'count':JN_o_number.values[:,0]})
num_time_df.columns=['TIME','number']
num_time_df.to_csv('JN_o_number.csv',index=False,encoding='utf_8_sig')
#JN_LuC.csv
dis_data_group=JN_LuC.groupby(['day','distance'])['distance'].count()
dis_data_group=dis_data_group.unstack()
dis_data_group.to_csv('JN_LuC.csv',index=True,encoding='utf_8_sig')
print('已全部完成，请在工作目录下查看是否已经生成JN_TIME_O.csv、JN_TIME_O_WEEK.csv、record.json、JN_5T_kmh.csv、JN_o_number.csv以及JN_LuC.csv')
