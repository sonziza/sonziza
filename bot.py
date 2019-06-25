# ---------------SonZiza-----------------#
#           April, 22, 2019
#   
#           
#   description:Авторизация на сайте и получение html-контента
#   ____________________________________
#   modue:    __________________________
#   classes:  __________________________
#   included files: ____________________
# ---------------------------------------#


import requests
import json

#функция авторизации на сайте
def loginbot(login, password):
    #Открываем сессию, через нее будем работать на сайте
    s = requests.Session()
    #массив передаваемых данных на сервер
    #получен через исследд-е элемента - вкладка Network - файл login
    data = {
        'lwa': '1',
        'log': login,
        'pwd': password,
        'lwa_profile_link': '1',
        'login-with-ajax': 'login'
    }
    #метод POST - отправим данные пользователя на сайт
    res = s.post('http://testq.mcdir.ru/wplogin.php', data=data)
    #JSON-обертка для удобочитаемого вида
    res2 = json.loads(res.text)
    # в случае успеха - читаем html-контент под авторизованным пользователем. Иначе - json-словарь
    if res2['result']==True:
        res2 = s.get('http://testq.mcdir.ru').text
    return res2

l = input('Ваш логин ')
p = input('Ваш пароль ')

print(loginbot(l, p))
