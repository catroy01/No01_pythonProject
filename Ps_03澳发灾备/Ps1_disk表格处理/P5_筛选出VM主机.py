# 导入pandas库
import pandas as pd

#读取excel文件
df=pd.read_excel('disk_count.xlsx')


#将hostname列作为DataFrame的一个列
df['hostname']=df['hostname'].astype(str)

#按照hostname列进行分组，获取每组的第一行数据，并保留第一列
result=df.groupby('hostname',sort=False).first().reset_index()

#保存结果到新的excel文件中
result.to_excel('disk_result.xlsx',index=False)