from flask import Flask, render_template
from flask_socketio import SocketIO
from dotenv import load_dotenv
from forms import Form
from flask_wtf.csrf import CSRFProtect
import os

from script import get_overall

# Load environment variables
load_dotenv()

# Initialize app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
csrf = CSRFProtect(app)

# Initialize socketio
socketio = SocketIO(app)

# Listen on submit
@socketio.on('submit')
def handle_submit(domain):
  overall = get_overall(domain, socketio)
  socketio.emit('overall_data', overall)

# Serve /
@app.route('/')
def index():
    form = Form()
    return render_template('index.html', form=form)

# Run app
if __name__ == '__main__':
  socketio.run(app)