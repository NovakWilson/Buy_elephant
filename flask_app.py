from flask import Flask, request
import logging
import json
import os
import requests

app = Flask(__name__)
APIKEY = 'trnsl.1.1.20200430T160157Z.57feabe2d5c38c3a.aabbb8850063014bb3e400a8fd5b429e8728eecb'
logging.basicConfig(level=logging.INFO)
sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info(f'Response: {response!r}')
    return json.dumps(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']
    if req['session']['new']:
        res['response']['text'] = 'Привет! Назови свое имя!'
        sessionStorage[user_id] = {
            'first_name': None,
            'game_started': False
        }
        return

    if sessionStorage[user_id]['first_name'] is None:
        first_name = get_first_name(req)
        if first_name is None:
            res['response']['text'] = 'Не расслышала имя. Повтори, пожалуйста!'
        else:
            sessionStorage[user_id]['first_name'] = first_name
            sessionStorage[user_id]['guessed_cities'] = []
            res['response']['text'] = 'Приятно познакомиться, {}. Я - Алиса. Ты можешь воспользоваться ' \
                                      'переводчиком. Для этого напиши: переведи слово "само слово"(без ковычек).'.format(first_name.title())
        return
    else:
        tokens = req['request']['nlu']['tokens']
        if tokens[0] == 'переведи' and tokens[1] == 'слово':
            if len(tokens[2]) == 1:
                res['response']['text'] = translate(tokens[2])
            else:
                string = ''
                for i in tokens[2:]:
                    string += i + ' '
                res['response']['text'] = translate(string)
        return


def translate(text):
    params = {'lang': 'en',
              'key': 'trnsl.1.1.20200430T160157Z.57feabe2d5c38c3a.aabbb8850063014bb3e400a8fd5b429e8728eecb',
              'text': text}
    res = requests.post(url='https://translate.yandex.net/api/v1.5/tr.json/translate', params=params).json()
    return res['text'][0]
    #print(json.dumps(res, indent=4))


def get_first_name(req):
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.FIO':
            return entity['value'].get('first_name', None)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
