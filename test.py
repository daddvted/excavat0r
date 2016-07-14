import re

s = "共2页 第1页 总记录数：30，跳转到第"


m = re.findall(r'(\d+)', s)
print(m)
