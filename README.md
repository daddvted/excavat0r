## 简单智能问答应用 [code: Excavator]
* 通过爬虫建立知识库
* 简单分析用户的问题
* 支持GET/POST/WebSocket请求方式
* 持续开发中...

`注意：GET请求需要将JSON数据放入HTTP的entity-body，但XMLHttpRequest不支持GET使用entity-body`
##### 请求JSON格式
```
{"msg":"大王叫我来巡山"}
```
##### 返回JSON格式
```
{"code":"000","resp":"大王 | 叫 | 我 | 来 | 巡山"}
{"code":"000","resp":[{"qid":1,"title":"你是谁？"},{"qid":2,"title":"到哪里去？"}]}
```
###### 返回码说明
code | 说明
---- | :----
000  | 问答返回正常
001  | 待定
400  | 用户确认提交问题给客服人员
900  | 问答返回异常

