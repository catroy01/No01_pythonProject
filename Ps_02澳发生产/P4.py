import pymysql
import pandas as pd

# 连接数据库
conn = pymysql.connect(host='172.25.192.101', user='exp_user', password='exp_123', database='zabbix', charset='utf8')
cursor = conn.cursor()

# 执行SQL查询语句
sql = """select 
t.their,t.cn_name,t.host,t.ip,t.memory,
100%-MAX(CASE t.key_ WHEN 'vm.memory.size[pavailable]' THEN t.value_avg_ ELSE 0 END) avg_mem 
from
(select i.key_,
h.name,
ah.their ,ah.cn_name , ah.host , ah.ip , ah.memory ,
AVG(hi.value_avg) value_avg_ 
from hosts h
join aofazaibei_hosts ah 
join interface inf on inf.ip = ah.ip 
join items i on h.hostid = i.hostid
join trends hi on i.itemid = hi.itemid
where
h.hostid = inf.hostid 	
and i.key_ in ('vm.memory.size[pavailable]')
and hi.clock >= unix_timestamp(20230201)
and hi.clock <= unix_timestamp(20230301)
group by h.name, i.key_ )
t group by t.name;"""

cursor.execute(sql)

# 将查询结果转换为DataFrame格式
data = pd.DataFrame(cursor.fetchall(), columns=['their', 'cn_name', 'host', 'ip', 'memory', 'avg_mem'])

# 将结果输出为Excel文件
with pd.ExcelWriter('result.xlsx') as writer:
    data.to_excel(writer, index=False, sheet_name='Sheet1')

# 关闭数据库连接
cursor.close()
conn.close()
