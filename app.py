from flask import Flask, render_template, redirect, request, session, url_for
from src.events import Events
import os, dotenv
from models import GitHub

dotenv.load_dotenv()
app = Flask(__name__)
events = Events(
    guild_id="818251363012182023",
    token=os.environ.get('DISCORD_TOKEN')
) 

app.secret_key = os.environ.get('APP_SECRET_KEY')

@app.route('/')
def index():
    elements = events.list
    return render_template('index.html', events=elements[:3])

@app.route('/login/auth')
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

@app.route('/login')
def login():
    github = GitHub()
    return redirect(github.login())

@app.route('/login/failed')
def login_failed():
    return "Login failed"

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('avatar', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)