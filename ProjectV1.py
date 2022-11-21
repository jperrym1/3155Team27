#SKELETON FOR PROJECT

import os
from flask import Flask
from flask import render_template
from flask import request, session
from flask import redirect, url_for
from database import db
from data_models import Project as Project
from data_models import User as User
from views import LoginView, RegisterView, CreateProjectView
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cubed_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SECRET_KEY'] = '311527'

db.init_app(app)

with app.app_context():
    db.create_all()

#main menu
@app.route('/')
@app.route('/index')
def index():
    if session.get('user'):
        return render_template('index.html', user=session['user'])
    return render_template('index.html')

#view list of projects
@app.route('/projects', methods=['GET', 'POST'])
def get_projects():
    if session.get('user'):
        projects = db.session.query(Project).filter_by(user_id=session['user_id']).all()
        return render_template('projects.html', user=session['user'], projects=projects)
    return redirect(url_for('login'))

#view particular project
@app.route('/projects/<project_id>')
def get_project(project_id):

    return render_template('project.html', project=projects[int(project_id)],user=tempUser)

#create project
@app.route('/projects/new', methods=['GET', 'POST'])
def create_project():
    if session.get('user'):
        form = CreateProjectView()
        if request.method == 'POST' and form.validate_on_submit():
            project_name = request.form['project_name']
            description = request.form['description']
            members = request.form['members']
            new_project = Project(project_name, description, session['user_id'], members)
            db.session.add(new_project)
            db.session.commit()
            return redirect(url_for('get_projects'))
        return render_template('new.html', form=form, user=session['user'])
    else:
        redirect(url_for('login'))


#edit project
@app.route('/projects/edit/<project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    if request.method == 'POST':
            name = request.form['name']
            description = request.form['projectDesc']
            members = request.form['projectMembers'].split(',')
            id = int(project_id)
            projects[id] = {'name': name, 'description': description, 'members': members}
            return redirect(url_for('get_projects'))
    else:
        project = projects[int(project_id)]
        return render_template('new.html', project=project, user=tempUser, project_id=project_id)
    return 1

#delete project
@app.route('/projects/delete/<project_id>', methods=['GET', 'POST'])
def delete_project(project_id):
    # key = projects.get(project_id, None)
    # if key:
    del projects[int(project_id)]
    return redirect(url_for('get_projects'))
    
@app.route('/login', methods=['GET','POST'])
def login():
    login = LoginView()
    if login.validate_on_submit():
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            # password match add user info to session
            session['user'] = the_user.first_name
            session['user_id'] = the_user.id
            # render view
            return redirect(url_for('get_projects'))

        # password check failed
        # set error message to alert user
        login.password.errors = ["Incorrect username or password."]
        return render_template("login.html", form=login)
    else:
        # form did not validate or GET request
        return render_template("login.html", form=login)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterView()
    if request.method == 'POST' and form.validate_on_submit():
        h_password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt()
        )
        first_name= request.form['firstname']
        last_name= request.form['lastname']
        new_user = User(first_name,last_name, request.form['email'], h_password)
        db.session.add(new_user)
        db.session.commit()
        session['user'] = first_name
        session['user_id'] = new_user.id
        return redirect(url_for('get_projects'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    if session.get('user'):
        session.clear()
    return redirect(url_for('index'))


app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)