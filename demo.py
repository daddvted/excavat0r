import redis

r = redis.StrictRedis(host="192.168.86.86", port=6379, db=0)

l = ["a", "b", "c"]
r.rpush("mylist2", *l)
