import requests

with open("target.txt", "r", encoding="utf-8") as file:
    content = file.read()

while True:
    r = requests.get(content)
    print(r.status_code)