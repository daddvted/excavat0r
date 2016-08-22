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
    template = "INSERT INTO juniorhighschool(name, addr, area, type, tel, website, overallmerit, "\
               "residence, scholarship, founded, code, sid, image, tuition) "\
               "VALUES (%(SchoolName)s, %(SchoolAddress)s, %(AreaName)s, %(SchoolType)s, %(SchoolTel)s,"\
               "%(SchoolUrl)s, %(OverallMerit)s, %(IsResidence)s, %(IsHaveScholarship)s, %(FoundedDate)s,"\
               "%(SchoolCode)s, %(Pid)s, %(ImagePath)s, %(Tuition)s)"
    cursor.execute(template, data)
    conn.commit()

with open("junior_high_school.txt", 'r') as f:
    raw = json.load(f)

school_list = json.loads(raw["data"])

for school in school_list:
    save2db(school)
