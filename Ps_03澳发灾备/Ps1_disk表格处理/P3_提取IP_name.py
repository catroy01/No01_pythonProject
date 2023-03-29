import pandas as pd

# 读取CPU.xlsx和IP_name.xlsx文件
cpu_df = pd.read_excel('disk_new02.xlsx')
ip_name_df = pd.read_excel('IP_name.xlsx')

# 合并CPU.xlsx和IP_name.xlsx文件，获取name列对应的IP地址
result = pd.merge(cpu_df, ip_name_df, on='IP', how='left')

# 保存结果到新的excel文件中
result.to_excel('disk_new03.xlsx', index=False)



