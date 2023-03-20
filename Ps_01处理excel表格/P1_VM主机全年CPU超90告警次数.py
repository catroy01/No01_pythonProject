import pandas as pd

# 读取 excel 文件
df = pd.read_excel('zabbix_CPU_event.xlsx')

# 去除年份小于等于2022年的记录
df = df[df.iloc[:,1] > '2022-01-01']

# 将 hostname 列作为 DataFrame 的一个列
df['hostname'] = df['hostname'].astype(str)

# 按照 hostname 列进行分组，获取每组的第一行数据，并保留第一列
result = df.groupby('hostname', sort=False).first().reset_index()

# 保存结果到新的 excel 文件中
result.to_excel('CPU.xlsx', index=False)
