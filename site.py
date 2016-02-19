from sys import argv

from bottle import run, get, post, error, static_file, request, response, view, default_app
from gz_middleware import GzMiddleware

@get('/css/whiteboard')
def css():
    return static_file('whiteboard.css', 'css/')

@get('/css/sensasans/<fontfile>')
def fonts(fontfile):
    return static_file(fontfile, "css/sensasans/")

@get('/js/<script:re:[A-Za-z]+>')
def js(script):
    return static_file(script + '.min.js', 'js/')

@get('/')
@view('index')
def index():
    return {}

@get('/board/new')
def newboard():
    board_id = '438pjaw34'
    redirect('/board/' + board_id)

@get('/board/<id:re:[A-Za-z0-9]+>')
@view('board')
def board(id):
    return {}


run(app=GzMiddleware(default_app()), host='0.0.0.0', port=8081, server='waitress', reloader='--debug' in argv, debug='--debug' in argv)
