# kanban/test_basic.py
from datetime import datetime
import os
import unittest
import sys

# find the right path to the directory
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.path.pardir)))
    
from kanban.models import Todo, User
from kanban import app, db
from flask_login import login_user
from flask_testing import TestCase

TEST_DB = 'testing.db'


class Pages(unittest.TestCase):

    def setUp(self):
        #set up before each run
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + TEST_DB
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        #after each test, get rid of the data
        db.session.remove()
        db.drop_all()

    def registration(self, username, email, password, confirm):
        # action: registration used for the tests
        return self.app.post(
            '/register',
            data=dict(username=username, email=email,
                      password=password, confirm=confirm),
            follow_redirects=True)

    def login(self, email, password):
        # action: login used for the tests
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True)

    def logout(self):
        # action: logout used
        return self.app.get(
            '/logout',
            follow_redirects=True)

    def test_home(self):
        #test: if the home page is working
        req = self.app.get('/', follow_redirects=True)
        self.assertEqual(req.status_code, 200)

    def test_registration(self):
        #test: if the registration page is working
        req = self.registration(
            'test-username', 'username@test.com', 'test123', 'test123')
        self.assertEqual(req.status_code, 200)

    def test_login_valid(self):
        #test: if the login page is working
        response = self.login('username@test.com', 'test123')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        #test: if the logout is working
        response = self.logout()
        self.assertEqual(response.status_code, 200)

class Functions(unittest.TestCase):

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        # setup for the tests to check the functionality
        self.app = app.test_client()
        db.create_all()
        self.user = User(username="test-username",
                         email="username@test.com", password="test123")
        db.session.add(self.user)
        todo = Todo(title="Task", description="Description",
                    deadline=datetime(2021, 3, 13, 0, 0), creator=self.user)
        db.session.add(todo)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_task(self):
        #test: if adding tasks works
        req = self.app.post('/add',
                            data=dict(title="New task",
                                      description="Description",
                                      deadline="2022-03-01",
                                      creator=self.user),
                            follow_redirects=True)
        self.assertEqual(req.status_code, 200)

    def test_move_to_do(self):
        #test: if moving tasks to "do" works
        req = self.app.get('/do/1', follow_redirects=True)
        self.assertEqual(req.status_code, 200)

    def test_move_to_done(self):
        #test: if moving tasks to "done" works
        req = self.app.get('/done/1', follow_redirects=True)
        self.assertEqual(req.status_code, 200)

    def test_move_to_todo(self):
        #test: if moving tasks to "to-do" works
        req = self.app.get('/todo/1', follow_redirects=True)
        self.assertEqual(req.status_code, 200)

    def test_delete(self):
        #test: if deleting tasks works
        req = self.app.get('/delete/1', follow_redirects=True)
        self.assertEqual(req.status_code, 200)

if __name__ == "__main__":
    unittest.main()
