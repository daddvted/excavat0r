# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import json
import codecs

class GIFPipeline(object):
    def __init__(self):
        self.file = codecs.open('done.json','w','utf-8')
    
    def process_item(self,item,spider):
        line = json.dumps(dict(item),ensure_ascii=False)+"\n"
        self.file.write(line)
