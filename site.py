from sys import argv

from bottle import run, get, post, error, static_file, request, response, view, default_app, redirect, HTTPResponse
from gz_middleware import GzMiddleware

from data_access import *

@get('/css/whiteboard')
def css():
    return static_file('whiteboard.css', 'css/')

@get('/css/sensasans/<fontfile>')
def fonts(fontfile):
    return static_file(fontfile, "css/sensasans/")

@get('/js/bliss')
def bliss():
    return static_file('bliss.js', 'js/libs/')

@get('/js/<script:re:[A-Za-z]+>')
def js(script):
    return static_file(script + '.min.js', 'js/')

@get('/')
@view('index')
def index():
    return {}

@get('/exists')
def exists():
    id = request.forms.id

    if id == ''
        abort(400)
    elif not Board.exists(id):
        abort(404)
    else:
        return HTTPResponse(200)


@post('/board/create/<id:re:^[A-Za-z0-9_-]+$>')
def create(id):
    board = Board(id)
    redirect('/board/' + id)

@get('/board/<id>')
def board():
    return {}

@post('/board/<id>/passphrase')
def passphrase(id):
    given_pass = request.forms.passphrase
    # TODO return whether passphrase is valid, return 200 or 403

run(app=GzMiddleware(default_app()), host='0.0.0.0', port=8081, server='waitress', reloader='--debug' in argv, debug='--debug' in argv)
