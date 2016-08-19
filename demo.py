import re
str = '远雄建设事业股份有限公司（FARGLORY LAND\r\r\n  DEVELOPMENT CO.,LTD.'
str = '远雄建设事业股份有限公司（abc'

print(re.sub(r'\r|\n', '', str))
print(str)



