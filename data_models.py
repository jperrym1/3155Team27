from database import db
import datetime
class User(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    first_name = db.Column('first_name', db.String(100))
    last_name = db.Column('last_name', db.String(100))
    email = db.Column('email', db.String(100))
    password = db.Column(db.String(255),nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    projects = db.relationship('Project', backref='user', lazy=True)
    #user_stories = db.relationship('UserStory', backref='user', lazy=True)
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.registered_on = datetime.date.today()

class Project(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column('title', db.String(200))
    description = db.Column('description', db.String(100))
    date = db.Column('date', db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    members = db.Column('members', db.String(255))
    views = db.Column('views', db.Integer)
    #testing here

    tasks = db.relationship('Task', backref='project', lazy = True)
    #user_stories = db.relationship('UserStory', backref='project', lazy=True)
    comments = db.relationship('Comment', backref='project', cascade='all, delete-orphan', lazy=True)
    
    def __init__(self, title, description, user_id, members):
        self.title = title
        self.description = description
        self.date = datetime.date.today()
        self.user_id = user_id
        self.members = members
        self.views = 0

class Task(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    description = db.Column('description', db.VARCHAR, nullable=False)
    completed = db.Column('completed', db.Integer)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    def __init__(self, description, project_id):
        self.description = description
        self.completed = 0
        self.project_id = project_id

class UserStory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False)
    date_closed = db.Column(db.DateTime)
    scenario = db.Column(db.VARCHAR, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, scenario, project_id, user_id):
        self.date_created = datetime.date.today()
        self.scenario = scenario
        self.project_id = project_id
        self.user_id = user_id

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.VARCHAR, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    def __init__(self, comment, project_id):
        self.comment = comment
        self.project_id = project_id