#SKELETON FOR PROJECT

import os
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/index')
def index():
    
    return render_template('index.html')
app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)