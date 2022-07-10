from flask import Flask, render_template
from src.events import Events
import os, dotenv

dotenv.load_dotenv()
app = Flask(__name__)
events = Events(
    guild_id="818251363012182023",
    token=os.environ.get("DISCORD_TOKEN")
) 

@app.route('/')
def index():
    elements = events.list
    return render_template('index.html', events=elements[:3])

if __name__ == "__main__":
    app.run(debug=True)