from flask import redirect, request, session, url_for
from src.models import GitHub


def login():
    github = GitHub()
    return redirect(github.login())

def auth():
    code = request.args.get('code')
    github = GitHub()
    token = github.auth(code)
    data = github.getData(token['access_token'])
    if data['login']:
        session['logged_in'] = True
        session['username'] = data['login']
        session['avatar'] = data['avatar_url']
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login_failed'))

def login_failed():
    return "Login failed"

def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('avatar', None)
    return redirect(url_for('index'))
