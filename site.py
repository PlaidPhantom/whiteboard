from re import match
from sys import argv

from bottle import run, get, post, error, static_file, request, response, view, default_app, redirect, abort, HTTPResponse
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

jsext = '.bundle.js' if '--debug' in argv else '.min.js'

@get('/js/<script:re:[A-Za-z]+>')
def js(script):
    return static_file(script + jsext, 'js/')

@get('/')
@view('index')
def index():
    return {}

@get('/exists')
def exists():
    id = request.query.id

    if id == '':
        abort(400)
    elif not Board.exists(id):
        abort(404)
    else:
        return HTTPResponse(status=200)


@post('/board/create')
def create():
    id = request.forms.id

    if id is None or id == "" or match('^[A-Za-z0-9_-]+$', id) is None:
        abort(400)

    Board.create(id)
    redirect('/board/' + id)

@get('/board/<id>')
@view('board')
def board(id):
    return { "board": Board(id) }

@post('/board/<id>/passphrase')
def passphrase(id):
    given_pass = request.forms.passphrase
    # TODO return whether passphrase is valid, return 200 or 403

run(app=GzMiddleware(default_app()), host='0.0.0.0', port=8081, server='waitress', reloader='--debug' in argv, debug='--debug' in argv)
