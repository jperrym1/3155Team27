#SKELETON FOR PROJECT

import os
from flask import Flask
from flask import render_template

app = Flask(__name__)

projects = {1: {'name': 'project1', 'description': 'first mock project on the list', 'members': 'Bob, Mark, Francine'},
            2: {'name': 'project2', 'description': 'second mock project', 'members': 'Sam, Gina, Tom'},
            3: {'name': 'project3', 'desciption': 'third mock project', 'members': 'Tina, Dana, Fred'} 
}

#main menu
@app.route('/')
@app.route('/index')
def index():
    
    return render_template('index.html')

#view list of projects
@app.route('/projects')
def get_projects():

    return render_template('projects.html', projects=projects)

#view particular project
@app.route('/projects/<project_id>')
def get_project():

    return render_template('project.html')

#create project
@app.route('/projects/new')
def create_project():

    return render_template('new.html')


#edit project
@app.route('/projects/edit/<project_id>')
def edit_project():

    return 1

#delete project
@app.route('/projects/delete/<project_id>')
def delete_project():

    return 1
    
app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)