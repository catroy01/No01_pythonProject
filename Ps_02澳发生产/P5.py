from zabbix_api import ZabbixAPI
import pandas as pd
from openpyxl import Workbook

# 连接到Zabbix API
zabbix_url = 'http://172.25.192.101/zabbix'
zabbix_user = 'admin'
zabbix_password = 'Gdspass12Tim123456'
zabbix = ZabbixAPI(url=zabbix_url, user=zabbix_user, password=zabbix_password)

# 查询所有的主机
hosts = zabbix.host.get(output=['name', 'host', 'status'])

# 将结果转换为Pandas数据帧，并按照名称排序
df_hosts = pd.DataFrame(hosts)
df_hosts = df_hosts.sort_values(by='name')

# 查询vm.memory.size[pavailable]监控项的item ID
items = zabbix.item.get(output='itemid', search={'key_': 'vm.memory.size[pavailable]'})

# 获取2022年12个月的时间戳范围
timestamps = pd.date_range(start='2022-01-01 00:00:00', end='2022-12-31 23:59:59', freq='MS')
timestamp_ranges = [(int(timestamp.timestamp()), int(timestamp.shift(months=1).timestamp()) - 1) for timestamp in timestamps]

# 查询每个月的监控项均值
results = []
for item in items:
    for timestamp_range in timestamp_ranges:
        history = zabbix.history.get(itemids=item['itemid'], history=0, time_from=timestamp_range[0], time_till=timestamp_range[1], output='extend')
        if len(history) > 0:
            values = [float(h['value']) for h in history]
            avg_value = sum(values) / len(values)
            results.append({'itemid': item['itemid'], 'month': timestamp_range[0], 'avg_value': avg_value})

# 将结果转换为Pandas数据帧，并按照监控项ID和月份排序
df_results = pd.DataFrame(results)
df_results = df_results.sort_values(by=['itemid', 'month'])

# 创建一个新的工作簿，并写入查询结果
wb = Workbook()
ws = wb.active

# 写入表头
ws.append(['Host name', 'Host IP'] + [timestamp.strftime('%Y-%m') for timestamp in timestamps])

# 循环查询每个主机的IP地址和每个月的监控项均值，并写入工作簿
for index, row in df_hosts.iterrows():
    hostid = zabbix.host.get(filter={'host': row['host']}, output='extend')[0]['hostid']
    host_ip = zabbix.hostinterface.get(hostids=hostid, output='extend')[0]['ip']
    ws.append([row['name'], host_ip] + df_results[df_results['itemid'] == item['itemid']]['avg_value'].tolist())

# 保存工作簿到文件
wb.save('zabbix_result.xlsx')
