from wsgiref.simple_server import make_server
import mimetypes
import os



def response_file(filepath, start_response):
    if os.path.isdir('page' + filepath) and os.path.isfile('page' + filepath + '/index.html'):
        start_response('200 OK', [('Content-type', 'text/html')])
        with open('page' + filepath + '/index.html', 'r') as f:
            return [f.read().encode('utf-8')]
    
    if os.path.isfile('page' + filepath):
        start_response('200 OK', [('Content-type', mimetypes.guess_type(filepath)[0])])
        with open('page' + filepath, 'r') as f:
            return [f.read().encode('utf-8')]
    
    start_response('404 Not Found', [])
    return b''



def app(environ, start_response):
    return response_file(environ['PATH_INFO'], start_response)



with make_server('', 8080, app) as httpd:
    print('Serving on port 8080')
    httpd.serve_forever()
