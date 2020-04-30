APIKEY = 'trnsl.1.1.20200430T160157Z.57feabe2d5c38c3a.aabbb8850063014bb3e400a8fd5b429e8728eecb'
from flask import Flask, request
import logging
import json
import os
import requests

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


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
    tokens = req['request']['nlu']['tokens']
    if tokens[0] == 'переведи' and tokens[1] == 'слово':
        res['response']['text'] = translate(tokens[2])
    return


def translate(text):
    params = {'lang': 'en',
              'key': 'trnsl.1.1.20200430T160157Z.57feabe2d5c38c3a.aabbb8850063014bb3e400a8fd5b429e8728eecb',
              'text': text}
    res = requests.post(url='https://translate.yandex.net/api/v1.5/tr.json/translate', params=params).json()
    print(json.dumps(res, indent=4))


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
