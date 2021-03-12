from flask import render_template, url_for, redirect, flash, request
from kanban import app, db, bcrypt
from kanban.models import Todo, User
from kanban.forms import reg_form, login_form
from sqlalchemy import and_, or_, not_
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime

# home page with all the tasks
@app.route("/", methods=['POST', 'GET'])
@login_required
def home():
    todo = Todo.query.filter_by(
        do=False, done=False, user_id=current_user.id).all()
    do = Todo.query.filter_by(
        do=True, done=False, user_id=current_user.id).all()
    done = Todo.query.filter_by(
        do=True, done=True, user_id=current_user.id).all()
    return render_template('home.html', todos=todo, dos=do, dones=done)

# adding new tasks
@app.route("/add", methods=['POST', 'GET'])
@login_required
def add_todo():

    title = request.form['title']
    description = request.form['description']
    deadline = request.form['deadline']

    # checking if all entries are not empty to only then add the task
    # I could also do this using wtforms, but I was curious how to it using normal ones
    if title != '' and description != '' and deadline != '':
        todo = Todo(title=title, description=description,
                    deadline=datetime.strptime(deadline, '%Y-%m-%d'), creator=current_user)
        db.session.add(todo)
        db.session.commit()
        flash(f'You created a new task ({todo.title})!', 'success')
    else:
        flash(f"Please fill out all of the fields!", "danger")
    return redirect(url_for('home'))

# moving tasks to todo
@app.route("/todo/<int:todo_id>")
def todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.do = False
    todo.done = False
    db.session.commit()
    flash(f"You have a new to-do task ({todo.title})!", "success")
    return redirect(url_for('home'))

# moving tasks to doing
@app.route("/do/<int:todo_id>")
def do(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.do = True
    todo.done = False
    db.session.commit()
    flash(f"You are now doing the task ({todo.title})!", "success")
    return redirect(url_for('home'))

# moving tasks to done
@app.route("/done/<int:todo_id>")
def done(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.do = True
    todo.done = True
    db.session.commit()
    flash(f"You have done the task ({todo.title})!", "success")
    return redirect(url_for('home'))

# deleting tasks
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    flash(f"You deleted the task ({todo.title})!", "danger")
    return redirect(url_for('home'))

# registering users
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = reg_form()
    if form.validate_on_submit():

        # generating the hashed password and storing it as so
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)

        # adding the user to the database
        db.session.add(user)
        db.session.commit()
        flash(
            f'Congrats on successful account creation, {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('reg.html', title="Register", form=form)

# logging users in
@app.route("/login", methods=['GET', 'POST'])
def login():
    # checking for authentication
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = login_form()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # checking whether the password matches based on the hashed representation
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            # If the user was in a page before logging in
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Please try logging in again!', 'danger')
    return render_template('login.html', title="Login", form=form)

# logging users out
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
