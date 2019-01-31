"""
成都小升初查询
URL: http://www.cdzsks.com/
URL: http://www.cdzsks.com/partition/partitioninfo
该程序将通过Postman获取的json数据,直接导入数据库
"""

import json
import mysql.connector

config = {
    'user': 'root',
    'password': 'hello',
    'host': '192.168.86.86',
    'port': '3306',
    'database': 'service_cd',
    'raise_on_warnings': True,

}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()


def save2db(data):
    template = "INSERT INTO primary2junior(name, area, zoneid, code, "\
               "junior_name, junior_code, junior_sid) "\
               "VALUES (%(name)s, %(area)s, %(zoneid)s, %(code)s,"\
               "%(junior_name)s, %(junior_code)s, %(junior_sid)s)"
    cursor.execute(template, data)
    conn.commit()

with open("primary2junior.txt", 'r') as f:
    raw = json.load(f)

school_list = json.loads(raw["data"])

for item in school_list:
    data = {
        "name": item["GraduateSchoolName"],
        "area": item["AreaName"],
        "zoneid": item["ID"],
        "code": item["SchoolCode"]
    }
    junior_list = json.loads(item["juniorSchoolList"])
    for junior in junior_list:
        data["junior_name"] = junior["SchoolName"]
        data["junior_code"] = junior["SchoolCode"]
        data["junior_sid"] = junior["Pid"]

        save2db(data)


