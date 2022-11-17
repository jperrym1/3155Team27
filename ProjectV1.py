#SKELETON FOR PROJECT

import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for

app = Flask(__name__)

projects = {1: {'name': 'project1', 'description': 'first mock project on the list', 'members': 'Bob, Mark, Francine'},
            2: {'name': 'project2', 'description': 'second mock project', 'members': 'Sam, Gina, Tom'},
            3: {'name': 'project3', 'description': 'third mock project', 'members': 'Tina, Dana, Fred'} 
}
tempUser = {'name': 'admin', 'email': 'admin@3cubed.com'}
#main menu
@app.route('/')
@app.route('/index')
def index():
    tempUser = {'name': 'admin', 'email': 'admin@3cubed.com'}

    return render_template('index.html', user=tempUser)

#view list of projects
@app.route('/projects')
def get_projects():

    return render_template('projects.html', projects=projects, user=tempUser)

#view particular project
@app.route('/projects/<project_id>')
def get_project(project_id):

    return render_template('project.html', project=projects[int(project_id)],user=tempUser)

#create project
@app.route('/projects/new')
def create_project():
    tempUser = {'name': 'admin', 'email': 'admin@3cubed.com'}

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        members = request.form['members']
        id = len(projects)+1
        projects[id] = {'name': name, 'description': description, 'members': members}
        return redirect(url_for('get_projects'))
    else:
        return render_template('new.html', user=tempUser)


#edit project
@app.route('/projects/edit/<project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    
    return 1

#delete project
@app.route('/projects/delete/<project_id>')
def delete_project(project_id):
    for i in projects:
        if projects[project_id] == projects[i]:
            del projects[i]
    return redirect(url_for('projects.html'))
    
app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)