import re
import json

with open("junior_high_school.txt", 'r') as f:
    tmp = json.load(f)


l = json.loads(tmp["data"])
print(len(l))
for item in l:
    print(item)

