import requests
import googletrans

from random import randint
from re import sub
from time import sleep

key = ''

def rand():
    return randint(10**20, 10**22)
    
def get_messages(chat):
    global key;
    url = 'https://discord.com/api/v8/channels/{}/messages'.format(chat)
    head = {'authorization': key}
    r = requests.get(url, params={'limit': 5}, headers=head)
    return r.json()

def send_message(chat, msg):
    global key;
    url = 'https://discord.com/api/v8/channels/{}/messages'.format(chat)
    head = {'authorization': key}
    data = {
        'content': msg,
        'nonce': rand(),
        'tts': False
    }
    r = requests.post(url, data=data, headers=head)
    data = r.json()
    return data['content']
    

def translate(text):
    translator = googletrans.Translator()
    
    langs = list(googletrans.LANGCODES.items())
    lang = langs[randint(0, len(langs) - 1)]
    result = translator.translate(text, dest=lang[1])
    return '{} {}'.format(lang[0], result.text)

def main():
    friend = '412999222351364106'
    last = 0
    
    while 1:
        data = get_messages(653879632755556352)
        for msg in data[::-1]:
            if msg['author']['id'] == friend:
                text = msg['content']
                if int(msg['id']) <= last:
                    continue
                last = int(msg['id'])
                pattern = '<@!\d+>'
                text = sub(pattern, '', text)
                if not text: continue
                res = translate(text)
                if not res: continue
                print(text, send_message(msg['channel_id'], res))
    
        sleep(5)

if __name__ == '__main__':
    main()