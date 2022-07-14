from flask import Flask, render_template, redirect, url_for
from src.events import Events
import os, dotenv
from flask_dance.contrib.github import make_github_blueprint, github

dotenv.load_dotenv()

app = Flask(__name__)

app.secret_key = os.environ.get("APP_SECRET_KEY")
print(os.environ.get("APP_SECRET_KEY"))

blueprint = make_github_blueprint(
    client_id=os.environ.get("GITHUB_CLIENT_ID"),
    client_secret=os.environ.get("GITHUB_CLIENT_SECRET")
)
app.register_blueprint(blueprint, url_prefix="/login")

events = Events(
    guild_id="818251363012182023",
    token=os.environ.get("DISCORD_TOKEN")
) 

@app.route('/')
def index():
    elements = events.list
    return render_template('index.html', events=elements[:3])

@app.route('/login')
def login():
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    assert resp.ok
    return "You are @{login} on GitHub".format(login=resp.json()["login"])

if __name__ == "__main__":
    app.run(debug=True)