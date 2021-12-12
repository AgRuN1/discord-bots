from requests import patch, get
from datetime import datetime
from time import sleep
from json import loads, dump, load
from time import time
from os import path

def get_emoji(desc):
    if 'обл' in desc:
        if 'ясн' in desc:
            return '⛅'
        return '☁️'
    if 'пасмурно' in desc:
        return '☁️'
    if 'дожд' in desc:
        if 'небольшой' in desc:
            return '🌦️'
        return '🌧️'
    if 'солн' in desc or 'ясно' in desc:
        return '☀️'
    if 'туман' in desc:
        return '🌫️'
    return ''

def get_status(city):
    freq = 1200
    last_req = freq
    data = ''
    if path.isfile(city):
        t = path.getmtime(city)
        last_req = round(time() - t)
    if last_req >= freq:
        appid = ''
        lang = 'ru'
        url = 'https://api.openweathermap.org/data/2.5/weather'
        res = get(url, params={'q': city, 'lang': lang, 'appid': appid})
        data = res.json()
        with open(city, 'w') as f:
            dump(data, f)
    else:
        with open(city) as f:
            data = load(f)
    desc = data['weather'][0]['description'].capitalize()
    speed = data['wind']['speed']
    temp = round(data['main']['temp'] - 273.15)
    tm = datetime.now().strftime('%H:%M:%S')
    sunrise = datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone']).strftime('%H:%M:%S') 
    sunset = datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone']).strftime('%H:%M:%S') 
    emoji_name = get_emoji(desc.lower())

    status = "{} в городе {} {}°C  Скорость ветра {} м/c Время восхода: {} Время захода: {} Текущее время: {}!".format(desc, data['name'], temp, speed, sunrise, sunset, tm)
            
    return {'custom_status': {'text': status, 'emoji_name': emoji_name}}

def main():
    url = 'https://discord.com/api/v8/users/@me/settings'
    key = ''
    head = {'authorization': key}
    my_city = 'Tver'
    while 1:
        payload = get_status(my_city)
        r = patch(url, json=payload, headers=head)
        res = loads(r.text)
        print(res)
        sleep(5)

if __name__ == '__main__':
    main()