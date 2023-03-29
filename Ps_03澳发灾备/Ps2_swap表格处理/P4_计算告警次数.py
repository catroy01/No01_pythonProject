# 导入pandas库
import pandas as pd

# 读取excel文件
df = pd.read_excel('swap_new03.xlsx')


# 将主机名列转换为DataFrame的列
df['hostname'] = df['hostname'].astype(str)

# 按主机名列分组，计算相同主机名出现的次数，并将其输出到新列中
df['count'] = df.groupby('hostname')['hostname'].transform('count')


# 将结果保存到新的excel文件中
df.to_excel('swap_count.xlsx', index=False)