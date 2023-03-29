from pyzabbix import ZabbixAPI
from datetime import datetime
from time import mktime, strptime

# 连接 Zabbix API
zabbix_server = 'http://172.24.192.101/zabbix'
zabbix_username = 'Admin'
zabbix_password = 'Gdspass12Tim123456'
zabbix = ZabbixAPI(zabbix_server)
zabbix.login(zabbix_username, zabbix_password)

# 设置内存使用率查询的时间范围
time_format = '%Y-%m-%d %H:%M:%S'
time_from = int(mktime(strptime('2022-01-01 00:00:00', time_format)))
time_till = int(mktime(strptime('2022-12-31 23:59:59', time_format)))
time_range = {"from": time_from, "to": time_till}

# 获取所有主机
hosts = zabbix.host.get(output=["hostid", "name"])

# 创建字典以存储每个主机每月的内存使用率
monthly_memory_usage = {
    'January': [],
    'February': [],
    'March': [],
    'April': [],
    'May': [],
    'June': [],
    'July': [],
    'August': [],
    'September': [],
    'October': [],
    'November': [],
    'December': []
}

# 遍历每个主机并获取每月的内存使用率
for host in hosts:
    host_id = host['hostid']
    items = zabbix.item.get(hostids=host_id, search={'key_': 'vm.memory.size'}, output=["itemid", "name"])
    for item in items:
        item_id = item['itemid']
        memory_usage = zabbix.history.get(itemids=[item_id], time_from=time_range['from'], time_till=time_range['to'],
                                          output='extend', limit=5000, history=0)
        for memory_item in memory_usage:
            date_time_str = memory_item['clock']
            date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            month = date_time_obj.strftime("%B")
            monthly_memory_usage[month].append(memory_item['lastvalue'])

# 打印每个主机每月的内存使用率
for host in hosts:
    host_name = host['name']
    print("Host: {}".format(host_name))
    for month, values in monthly_memory_usage.items():
        if not values:
            continue
        avg_usage = sum(values) / len(values)
        print("{}: {:.2f}%".format(month, avg_usage))
    print("\n")
