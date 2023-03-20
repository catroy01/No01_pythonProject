# 导入pandas库
import pandas as pd

# 读取excel文件
df = pd.read_excel('zabbix_CPU_event.xlsx')

# 分析time列格式 :YYYY-mm-dd hh:mm:ss - YYYY-mm-dd hh:mm:ss
try:
    df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S')
except ValueError as e:
    print(e)
df['time_diff'] = df['time'].diff()

# 计算这两个时间的相减
print(df['time_diff'])
