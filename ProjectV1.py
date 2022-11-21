#SKELETON FOR PROJECT

import os
from flask import Flask
from flask import render_template
from flask import request, session
from flask import redirect, url_for
from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cubed_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SECRET_KEY'] = '311527'

db.init_app(app)

with app.app_context():
    db.create_all()

projects = {1: {'name': 'project1', 'description': 'first mock project on the list', 'members': ['Bob', 'Mark', 'Francine']},
            2: {'name': 'project2', 'description': 'second mock project', 'members': ['Sam', 'Gina', 'Tom']},
            3: {'name': 'project3', 'description': 'third mock project', 'members': ['Tina', 'Dana', 'Fred']} 
}
tempUser = {'name': 'admin', 'email': 'admin@3cubed.com'}
#main menu
@app.route('/')
@app.route('/index')
def index():
    if session.get('user'):
        return render_template('index.html', user=session['user'])
    return render_template('index.html')

#view list of projects
@app.route('/projects')
def get_projects():
    if session.get('user'):
        projects = db.session.query()
        return render_template('projects.html', user=session['user'])
    return render_template('projects.html', projects=projects, user=tempUser)

#view particular project
@app.route('/projects/<project_id>')
def get_project(project_id):

    return render_template('project.html', project=projects[int(project_id)],user=tempUser)

#create project
@app.route('/projects/new', method=['GET', 'POST'])
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
    if request.method == 'POST':
            name = request.form['name']

            desc = request.form['projectDesc']
            
            return redirect(url_for('get_projects'))
    else:
        project = projects[int(project_id)]
        return render_template('new.html', project=project, user=tempUser)
    return 1

#delete project
@app.route('/projects/delete/<project_id>')
def delete_project(project_id):
    for i in projects:
        if projects[project_id] == projects[i]:
            del projects[i]
    return redirect(url_for('projects.html'))
    
app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)