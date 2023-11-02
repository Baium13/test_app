from flask import Flask
import json
app = Flask(__name__)

a = {'username': 'vova', 'islogin': True}
b = '{"username":"vova", "islogin":true}'
print(json.loads(b))
from log import app
@app.route("/")
def hello():
    return "Hello, World!"


if __name__ == '__main__':
    app.run()

"""
1)Зробити енд поинт POST  /login який будет приймати юзернейм и пароль на вхід а на вихід буде давати "ок" 
або "логин фейлд"
список логінів і паролів буде в списку на сервері
2)Зробити інший скрип в index.py  який буде робити запит на 127.0.0.1:5000.
-http 
-примери кодов
-flsak как он работает
-jason
3)Всі логіни і паролі повинні бути вичітані с джейсон файла
 
"""
