## 简单智能问答API [code: Excavator]
* 通过爬虫建立知识库
* 简单分析用户的问题
* 支持GET/POST/WebSocket请求方式
* 持续开发中...

`注意：GET请求需要将JSON数据放入HTTP的entity-body，但XMLHttpRequest不支持GET使用entity-body`
##### 请求JSON格式
```
{"msg":"大王叫我来巡山"}
```
##### 返回码及对应JSON说明
```
[ 000 ] - 返回正常回答
{"code":"000","resp":"大王 | 叫 | 我 | 来 | 巡山"} //返回正常回答
{"code":"000","resp":[{"qid":1,"title":"你是谁？"},{"qid":2,"title":"到哪里去？"},...]}

[ 001 ] - 单关键字返回，包含"kw"来进行新的搜索或地图搜索
{"code":"001","resp":{"text":"blabla","kw":"这是搜索关键字"}}

[ 002 ] - 地址查询
{"code":"002","resp":{"kw":"XX局"}

[ 400 ] - 未能回答问题提交给后台

[ 900 ] - 用户提问不在系统范围
```

