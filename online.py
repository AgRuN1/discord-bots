from requests import get, patch
from datetime import datetime
from time import sleep

prev = 0

def get_emoji(current):
    global prev;
    value = '☑️'
    if prev == 0:
        prev = current
        return value
        
    if current > prev:
        value = '⬆️'
    elif current < prev:
        value = '⬇️'
        
    prev = current
    return value

def get_online(appid):
    url = 'http://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1'
    data = {'format': 'json', 'appid': appid}
    r = get(url, params=data)
    data = r.json()
    return data['response']['player_count']

def frm(digit):
    data = str(digit)
    res = ''
    for i,c in enumerate(data[::-1]):
        if i % 3 == 0 and i:
            res = ' ' + res
        res = c + res
    return res

def main():
    url = 'https://discord.com/api/v8/users/@me/settings'
    key = 's'
    head = {'authorization': key}
    try:
        while 1:
            onl1 = get_online(570940)
            onl2 = get_online(335300)
            onl3 = get_online(374320)
            text = 'Current online in DSR: {}, DS 2 SotFS: {}, DS3: {}!'.format(frm(onl1), frm(onl2), frm(onl3))
            emoji_name = get_emoji(onl1 + onl2 + onl3)
            payload = {'custom_status': {'text': text, 'emoji_name': emoji_name}}
            r = patch(url, json=payload, headers=head)
            res = r.json()
            tm = datetime.now().strftime('%H:%M')
            print(tm, res['custom_status']['text'])
            sleep(300)
    except KeyboardInterrupt:
        payload = {'custom_status': {'text': ''}}
        r = patch(url, json=payload, headers=head)
        print('Статус сброшен, закрытие бота')
        exit()

if __name__ == '__main__':
    main()