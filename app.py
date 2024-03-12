from flask import Flask, render_template, request, Response
from dotenv import load_dotenv
from forms import Form
from flask_wtf.csrf import CSRFProtect
import threading
import os

from script import get_overall

# Load environment variables
load_dotenv()

# Initialize app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
csrf = CSRFProtect(app)

# Listen on submit
@app.route('/get_overall', methods=['POST'])
def process():
  uni_url = request.json

  def run_in_thread():
    with app.app_context():
      return Response(get_overall(uni_url), mimetype='application/json')
    
  thread = threading.Thread(target=run_in_thread)
  thread.start()

# Serve /
@app.route('/')
def index():
  print("App started")
  form = Form()
  return render_template('index.html', form=form)

# Run app
if __name__ == '__main__':
  app.run()