import pandas as pd

# 读取CPU_new02.xlsx和hosts_IP.xlsx文件
cpu_df = pd.read_excel('disk_new01.xlsx')
ip_name_df = pd.read_excel('hosts_IP.xlsx')

# 合并CPU_new02.xlsx和hosts_IP.xlsx文件
result = pd.merge(cpu_df, ip_name_df, on='hostname', how='left')

# 将合并结果存储到新的excel文件中
result.to_excel('disk_new02.xlsx', index=False)
