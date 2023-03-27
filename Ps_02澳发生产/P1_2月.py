from pyzabbix import ZabbixAPI
import pandas as pd

# 连接到Zabbix API
zapi = ZabbixAPI("http://172.24.192.101/zabbix")
zapi.login("Admin", "Gdspass12Tim123456")

# 获取所有主机
hosts = zapi.host.get(output=["name", "host"], selectInterfaces=["ip"])

# 存储结果的列表
result = []

for host in hosts:
    # 获取主机ID
    host_id = host['hostid']
    # 获取2月份的内存使用率
    memory_usage = zapi.item.get(
        search={"key_": "vm.memory.size[pavailable]"},
        hostids=host_id,
        output=["lastvalue"],
        # 设置时间范围为2月
        time_range={"from": "2022-03-01 00:00:00", "to": "2022-03-30 23:59:59"}
    )
    if memory_usage and memory_usage[0]['lastvalue'] != 'N/A':
        memory_usage = memory_usage[0]['lastvalue'] + '%'
    else:
        memory_usage = ''

    # 将结果添加到列表中
    result.append({
        "Name": host['name'],
        "IP": host['interfaces'][0]['ip'],
        "Memory Usage": memory_usage
    })

# 将结果写入Excel文件
df = pd.DataFrame(result)
df.to_excel('memory_usage202203.xlsx', index=False)
