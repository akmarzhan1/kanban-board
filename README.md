# Kanban-Board
A Kanban board designed as part of my CS162 assignment during Spring 2021. 

**Keywords**: Python, Flask, HTML, CSS, SQL. 


# Kanban Board
Below is a screenshot of the implementation with three sections: "To-do", "Doing," and "Done." The app can:
* create new tasks (with description and due date);
* move tasks from any column to any other column (e.g., from "Done" to "To-do");
* delete tasks from any column;
* log in users;
* log out users;
* register new users.

Below is the screenshot from the main page:
<img width="1175" alt="Screen Shot 2021-03-13 at 06 03 35" src="https://user-images.githubusercontent.com/47840436/111010834-daefaf80-83c1-11eb-9abd-d66cf8fdd12d.png">

# Setting up the database
I am using sqlite database and, in theory, you can use the one I have created and just write over it, but you could also create your own by:
```python
python3
from kanban import db
db.drop_all()
db.create_all()
```



# Run the code
Open your terminal or CMD and type the following from the cs162-kanban root directory.
```python
python -m venv .venv 
source .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=run.py
flask run
```

Then, your app will run at http://127.0.0.1:5000/, which you can easily access through your browser. 

# Unit tests
Go to the kanban root directory and run the following:
```python
python test.py
```

You should get something like the below:


<img width="508" alt="Screen Shot 2021-03-13 at 05 59 40" src="https://user-images.githubusercontent.com/47840436/111010637-4edd8800-83c1-11eb-8a56-75a0a9e13153.png">


# Project Structure

```
path/kanban-board
├── kanban/
│   ├── __init__.py
│   ├── forms.py
│   ├── models.py
│   ├── routes.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── login.html
│   │   └── reg.html
│   ├── static/
│   │   ├── favi.ico
│   │   └── styling.css
│   ├── data.db
│   ├── test.db
│   └── test.py
├── README.md
├── requirements.txt
└── run.py

```

### References
Creating a Todo List App With Flask and Flask-SQLAlchemy: https://www.youtube.com/watch?v=4kD-GRF5VPs

WTForm Documentation: https://wtforms.readthedocs.io/en/2.3.x/

SQL Alchemy Documentation: https://www.sqlalchemy.org/
