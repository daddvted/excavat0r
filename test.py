
sql = "INSERT INTO abc (name, age) VALUES" \
      "('{user_name}', {age})"


data = {
    "user_name": "skipper",
    "age": 30,
}

print(sql.format(**data))