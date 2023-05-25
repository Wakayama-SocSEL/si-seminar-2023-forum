from socketserver import ThreadingMixIn
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server, WSGIServer

import copy
import hashlib
import json
import subprocess
import time

import judge



"""
[
    {
        'player_id': 送信プレイヤの固有文字列,
        'body': メッセージ本文,
        'ng': 送信プレイヤのNG行動,
        'judge': 'アウト' or 'セーフ',
    }
    ...
]
"""
messages = []



"""
{
    クライアントから送信されるトークン文字列: {
        'player_id': プレイヤの固有文字列,
        'ng': プレイヤのNG行動,
        'checker': NG行動を判定する関数（引数は判定したいメッセージ）,
        'sequence': 最後に返答したときのメッセージ数
    }
    ...
]
"""
players = {}



# URLに応じて返答する
class App:
    def __init__(self, start_response):
        self.start_response = start_response
    
    

    def read_messages(self, token):
        if token in players:
            # 最大1時間待つ
            for _ in range(3600):
                # 前回の返答からメッセージが増えるまで返答を待機する
                if players[token]['sequence'] < len(messages):
                    break
                time.sleep(1)
            
            players[token]['sequence'] = len(messages)
        else:
            # 新しいプレイヤの追加
            ng, checker = judge.get_random_NG()
            players[token] = {
                'player_id': hashlib.md5(token.encode('utf-8')).hexdigest(),
                'ng': ng,
                'checker': checker,
                'sequence': len(messages)
            }
        
        # 受信プレイヤのNG行動を隠して返答する
        result_messages = copy.deepcopy(messages)
        for message in result_messages:
            if message['player_id'] == players[token]['player_id']:
                message['ng'] = '?'
        
        self.start_response('200 OK', [('Content-type', 'application/json')])
        return [json.dumps(result_messages).encode('utf-8')]



    def insert_message(self, message):
        messages.append({
            'player_id': players[message['token']]['player_id'],
            'body': message['body'],
            'ng': players[message['token']]['ng'],
            'judge': "アウト" if players[message['token']]['checker'](message['body']) else 'セーフ',
        })
        self.start_response('200 OK', [('Content-type', 'application/json')])
        return b''



    def index_html(self):
        self.start_response('200 OK', [('Content-type', 'text/html')])
        with open('page/index.html', 'r') as f:
            return [f.read().encode('utf-8')]



    def main_js(self):
        self.start_response('200 OK', [('Content-type', 'text/javascript')])
        with open('page/main.js', 'r') as f:
            return [f.read().encode('utf-8')]



    def style_css(self):
        self.start_response('200 OK', [('Content-type', 'text/css')])
        with open('page/style.css', 'r') as f:
            return [f.read().encode('utf-8')]



    def not_found(self):
        self.start_response('404 Not Found', [])
        return b''



def app(environ, start_response):
    response = App(start_response)
    query = parse_qs(environ['QUERY_STRING'])
    # URLに応じて返答する
    if environ['PATH_INFO'] == '/':
        return response.index_html()
    elif environ['PATH_INFO'] == '/main.js':
        return response.main_js()
    elif environ['PATH_INFO'] == '/style.css':
        return response.style_css()
    elif environ['PATH_INFO'] == '/messages':
        return response.read_messages(query['token'][0])
    elif environ['PATH_INFO'] == '/post':
        return response.insert_message(json.loads(environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', 0)))))
    else:
        return response.not_found()



# サーバを起動する
with make_server('', 8080, app, type('', (ThreadingMixIn, WSGIServer), {})) as httpd:
    subprocess.run('echo Serving on https://8080-$WEB_HOST', shell=True)
    httpd.serve_forever()
