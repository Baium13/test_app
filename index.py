import requests

url = 'http://127.0.0.1:5000/login'

data = {
    'username': 'Volodymyr',
    'password': '123456789'
}

headers = {
    'Content-type': 'application/json',
    'Accept': 'application/json'
}
response = requests.post(url, headers=headers, json=data)

session = requests.Session()
session.post()
session.get()

if response.status_code == 200:
    print("POST запрос успешный")
    print("Контент запроса:", response.text)
else:
    print("POST ошибка запроса статус кода:", response.status_code)
