from kanban import db, login_manager
from datetime import datetime
from flask_login import UserMixin

# the original database specification for keeping track of the tasks
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    do = db.Column(db.Boolean, default=False)
    done = db.Column(db.Boolean, default=False)
    deadline = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# user database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    todos = db.relationship('Todo', backref="creator", lazy=True)
