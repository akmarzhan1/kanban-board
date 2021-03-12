from kanban import db, login_manager
from flask_login import UserMixin
from datetime import datetime

# user database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    todos = db.relationship('Todo', backref="creator", lazy=True)

# the original database specification for keeping track of the tasks
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    do = db.Column(db.Boolean, default=False)
    done = db.Column(db.Boolean, default=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
