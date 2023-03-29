import requests
import json
import re
import time
import pandas as pd
from collections import defaultdict

class ZabbixApi:
    def __init__(self, ip, user, passwd):
        self.url = 'http://' + ip + '/zabbix/api_jsonrpc.php'
        self.user = user
        self.passwd = passwd
        self.headers = {'Content-Type': 'application/json-rpc'}
        self.__login()

    def request_data(self, key, host="", hostid="", templates="", templateid=""):
        data = {
            "USER_LOGIN": {
                "jsonrpc": "2.0",
                "method": "user.login",
                "params": {
                    "user": self.user,
                    "password": self.passwd},
                "auth": None,
                "id": 1,
            },
            "HOST_GET": {
                "method": "host.get",
                "params": {
                    # "output": "extend",
                    # "filter": {
                    #     "ip": host,
                    # },
                    "output": ["hostid", "host", "name", "status", "available"],
                    # status: 0-（默认）启用的；1-禁用的
                    # available: Zabbix agent的可用性，0-（默认）未知；1-可用；2-不可用
                    "selectInterfaces": ["interfaceid", "type", "ip"],
                    "selectGroups": "extend",
                    "selectParentTemplates": [
                        "templateid",
                        "name",]
                    }
            },
            "ITEM_GET": {
                "method": "item.get",
                "params": {
                    # "output": "extend",
                    "output": ["itemid", "name", "key_", "status", "state", "flags"],
                    # status: 0-（默认）启用的；1-禁用的
                    # state: 0-（默认）正常的；1-不支持的
                    # flags: 0-普通item；4-自动发现item
                    "hostids": hostid,
                    # "search": {
                    #     "key_": "apache"
                    # },
                    "sortfield": ["name"],}
            },
            "TEMPLATE_GET": {
                "method": "template.get",
                "params": {
                    "output": ["templateid", "name",],
                    "filter": {
                        "host": templates,
                    "parentTemplateid": "extend",
                }}
            },
            "USERMACRO_GET": {
                "method": "usermacro.get",
                "params": {
                    "output": "extend",
                    "hostids": templateid
                },
            },
            "EVENT_GET": {
                "method": "event.get",
                "params": {
                    "output": "extend",
                    "select_acknowledges": "extend",
                    "selectTags": "extend",
                    "hostids": hostid,
                    "sortfield": ["clock", "eventid"],
                    "sortorder": "DESC"
                },
            }
        }
        return data[key]

    def requester(self):
        try:
            response = requests.post(self.url, headers=self.headers, data=json.dumps(self.data))
            # print(response.json())
            return response.json()
        except Exception as e:
            print(e)
            raise Exception

    def __login(self):
        data = self.request_data("USER_LOGIN")
        self.data = data
        self.data.update({"auth": self.requester()["result"]})

    def host_get(self):
        data = self.request_data("HOST_GET")
        self.data.update(data)
        return self.requester()

    def item_get(self, hostid):
        data = self.request_data("ITEM_GET", hostid=hostid)
        self.data.update(data)
        return self.requester()

    def template_get(self, templates):
        data = self.request_data("TEMPLATE_GET", templates=templates)
        self.data.update(data)
        return self.requester()

    def usermacro_get(self, templateid):
        data = self.request_data("USERMACRO_GET", templateid=templateid)
        self.data.update(data)
        # print(self.data)
        return self.requester()

    def event_get(self, hostid):
        data = self.request_data("EVENT_GET", hostid=hostid)
        self.data.update(data)
        return self.requester()

def write_excel(filename, datas):
    df = pd.DataFrame(columns=("hostname", "time", "eventname"))
    for i, d in enumerate(datas, start=1):
        df.loc[i] = d
    df.to_excel(filename, sheet_name="event", index=False)
    # with pd.ExcelWriter(filename, mode="a") as writer:
    #     df.to_excel(writer, sheet_name="DR", index=False)

def get_datas():
    zabbix_ip = '172.25.192.101'
    user = 'Admin'
    password = 'Gdspass12Tim123456'
    zbx = ZabbixApi(zabbix_ip, user, password)
    host_result = zbx.host_get()["result"]

    templates = ["GDS18_Template OS Linux", "GDS18_Template OS Windows"]
    os_host = [i for i in host_result if any(x["name"] in templates for x in i["parentTemplates"])]
    print(len(os_host))
    # print(zbx.event_get(10280))
    #
    event_filters=["Disk space usage"] #Disk space usage ：CPU Utilization  ： Free swap : Available memory

    datas = []
    for i, host in enumerate(os_host, start=1):
        hostid = host["hostid"]

        hostname = host["name"]
        print(str(i), hostname)
        events = zbx.event_get(hostid)["result"]
        event_problem=[]
        event_ok=[]
        for event in events:
            if not any(i in event["name"] for i in event_filters):
                continue
            # 1:problem 0:OK
            if event["value"] == "1":
                # print("Problem: ", event)
                event_problem.append([event["r_eventid"], event["clock"], event["name"]])
            else:
                # print("Ok: ", event)
                event_ok.append([event["eventid"], event["clock"]])

        # print(event_problem)
        # print(event_ok)

        start_clock=""
        end_clock=""
        if len(event_problem) > 0:
            for ep in event_problem:
                start_clock = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(ep[1])))
                for eo in event_ok:
                    if ep[0] == eo[0]:
                        end_clock = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(eo[1])))
                        break
                else:
                    print("告警%s没恢复哦" %ep[2])
                datas.append([hostname, ' - '.join([start_clock, end_clock]), ep[2]])
    return datas


if __name__ == '__main__':
    datas = get_datas()
    write_excel("表格/zabbix_disk_event.xlsx", datas)