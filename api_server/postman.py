import requests
import json

data = {
    "email": "asdasdasd@gmail.com",
    "password": "asd123",
    "two_fa": "asdasdsadasd",
    "token": "asdasdasdasd34",
    "profile_name": "asdasdasdasd"
}
r = requests.post("http://127.0.0.1:5555/discord/add", data=json.dumps(data))
print(r.text)
