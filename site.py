from sys import argv

from bottle import run, get, post, error, static_file, request, response, view, default_app, redirect
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

@post('/board/new')
def newboard():
    board_id = request.forms.newid
    passphrase = request.forms.passphrase
    # TODO create board
    redirect('/board/' + board_id)

@post('/board/join')
def join():
    # TODO make sure board id is valid
    # TODO if board doesn't exist, offer to create
    redirect("/board/" + request.forms.id)

@get('/board/<id>')
def board():
    return {}

@post('/board/<id>/passphrase')
def passphrase(id):
    given_pass = request.forms.passphrase
    # TODO return whether passphrase is valid, return 200 or 403

run(app=GzMiddleware(default_app()), host='0.0.0.0', port=8081, server='waitress', reloader='--debug' in argv, debug='--debug' in argv)
