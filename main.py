from wsgiref.simple_server import make_server, WSGIServer
from urllib.parse import parse_qs
from socketserver import ThreadingMixIn
import time
import json
import subprocess



messages = []
token_length = {}



def save_log(message):
    subprocess.run(f"echo {message} >> message.log", shell=True)



class App:
    def __init__(self, start_response):
        self.start_response = start_response
    
    

    def read_item(self, token):
        if token in token_length:
            for _ in range(3600):
                if token_length[token] < len(messages):
                    break
                time.sleep(1)
        
        token_length[token] = len(messages)
        self.start_response('200 OK', [('Content-type', 'application/json')])
        return [json.dumps(messages).encode('utf-8')]



    def insert_message(self, message):
        messages.append(message)
        self.start_response('200 OK', [('Content-type', 'application/json')])
        print(len(messages))
        return [json.dumps({"status": "done"}).encode('utf-8')]



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



class ThreadingWSGIServer(ThreadingMixIn, WSGIServer):
    pass



def app(environ, start_response):
    response = App(start_response)
    query = parse_qs(environ['QUERY_STRING'])

    match environ['PATH_INFO']:
        case '/':
            return response.index_html()
        case '/main.js':
            return response.main_js()
        case '/style.css':
            return response.style_css()
        case '/messages':
            return response.read_item(query['token'][0])
        case '/post':
            return response.insert_message(json.loads(environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', 0)))))
        case _:
            return response.not_found()



with make_server('', 8080, app, ThreadingWSGIServer) as httpd:
    print('Serving on port 8080')
    httpd.serve_forever()
