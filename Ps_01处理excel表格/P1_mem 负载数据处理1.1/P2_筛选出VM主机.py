# 导入pandas库
import pandas as pd

#读取excel文件
df=pd.read_excel('memory_new01.xlsx')

#去除年份小于等于2022年的记录和大于2022年的记录
df=df[(df.iloc[:,1]>'2022-01-01')&(df.iloc[:,1]<'2023-01-01')]

#将hostname列作为DataFrame的一个列
df['hostname']=df['hostname'].astype(str)

#按照hostname列进行分组，获取每组的第一行数据，并保留第一列
result=df.groupby('hostname',sort=False).first().reset_index()

#保存结果到新的excel文件中
result.to_excel('memory_new02.xlsx',index=False)