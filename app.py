from flask import Flask
import os, dotenv
from routes import ROOT

dotenv.load_dotenv()
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000
app.secret_key = os.environ.get('APP_SECRET_KEY')

# Register the routes
for route in ROOT:
    app.route(
        rule=route["path"],
        methods=route["methods"]
    )(route['func'])

if __name__ == "__main__":
    app.run(debug=True)