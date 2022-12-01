#SKELETON FOR PROJECT

import os
from flask import Flask
from flask import render_template
from flask import request, session
from flask import redirect, url_for
from database import db
from data_models import Project as Project
from data_models import User as User
from data_models import Comment as Comment
from views import LoginView, RegisterView, CreateProjectView, CommentOnProject
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
    if session.get('user'):
        project = db.session.query(Project).filter_by(id=project_id, user_id=session['user_id']).one()
        form = CommentOnProject()
        return render_template('project.html', project=project,user=session['user'], form=form)

#create project
@app.route('/projects/new', methods=['GET', 'POST'])
def create_project():
    if session.get('user'):
        form = CreateProjectView()
        if request.method == 'POST' and form.validate_on_submit():
            project_name = request.form['project_name']
            description = request.form['description']
            members = request.form['members']

            #considering adding "tasks" and/or "tags" features as an added feature
            #tasks would act as the checklist while tags would act as identifiers or labels
            tasks = request.form['tasks']

            new_project = Project(project_name, description, session['user_id'], members, tasks)
            db.session.add(new_project)
            db.session.commit()
            return redirect(url_for('get_projects'))
        return render_template('new.html', form=form, user=session['user'])
    else:
        return redirect(url_for('login'))


#edit project
@app.route('/projects/edit/<project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    if session.get('user'):
        form = CreateProjectView()
        if request.method == 'POST':
            project_name = request.form['project_name']
            description = request.form['description']
            members = request.form['members']
            modified_project = db.session.query(Project).filter_by(id=project_id).one()
            modified_project.title = project_name
            modified_project.description = description
            modified_project.members = members
            db.session.add(modified_project)
            db.session.commit()
            return redirect(url_for('get_projects'))
        else:
            project = db.session.query(Project).filter_by(id=project_id).one()
            form.members.data = project.members
            form.project_name.data = project.title
            form.description.data = project.description
            return render_template('new.html', form=form, user=session['user'], project=project)
    else:
        return redirect(url_for('login'))

#delete project
@app.route('/projects/delete/<project_id>', methods=['POST'])
def delete_project(project_id):
    if session.get('user'):
        my_project = db.session.query(Project).filter_by(id=project_id).one()
        db.session.delete(my_project)
        db.session.commit()
        return redirect(url_for('get_projects'))
    else:
        return redirect(url_for('login'))
    
@app.route('/login', methods=['GET','POST'])
def login():
    login = LoginView()
    if login.validate_on_submit():
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            # password match add user info to session
            session['user'] = the_user.first_name
            session['user_id'] = the_user.id
            return redirect(url_for('get_projects'))
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

@app.route('/projects/<project_id>/comment', methods=['GET','POST'])
def project_comment(project_id):
    if session.get('user'):
        comment = CommentOnProject()

        if comment.validate_on_submit() and request.method=='POST':
            comment_text = request.form['comment']
            new_comment = Comment(comment_text, project_id)
            db.session.add(new_comment)
            db.session.commit()
        return redirect(url_for('get_project', project_id=project_id))
    else:
        return redirect(url_for('login'))

app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)