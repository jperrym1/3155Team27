#SKELETON FOR PROJECT

import os
from flask import Flask
from flask import render_template

app = Flask(__name__)

#main menu
@app.route('/index')
def index():
    
    return render_template('index.html')

#view list of projects
@app.route('/projects')
def get_projects():

    return 1

#view particular project
@app.route('/projects/<project_id>')
def get_project():

    return 1

#create project
@app.route('/projects/new')
def create_project():

    return 1


#edit project
@app.route('/projects/edit/<project_id>')
def edit_project():

    return 1

#delete project
@app.route('/projects/delete/<project_id>')
def delete_project():

    return 1
    
app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)