""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

class Task(db.Model):
    __tablename__ = 'tasks'  # Defines the table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    _title = db.Column(db.String(255), nullable=False)  # Task title column, cannot be null
    _description = db.Column(db.Text, nullable=True)  # Task description column, can be null
    _priority = db.Column(db.String(50), nullable=False)  # Task priority column, cannot be null
    _user_id = db.Column(db.Integer, nullable=False)  # Foreign key to user ID, cannot be null

    def __init__(self, title, description, priority, user_id):
        self._title = title
        self._description = description
        self._priority = priority
        self._user_id = user_id

    @property
    def title(self):
        return self._title
    @title.setter
    def name(self, title):
        self._title = title

    @property
    def description(self):
        return self._description
    @description.setter
    def name(self, description):
        self._description = description

    @property
    def priority(self):
        return self._priority
    @priority.setter
    def name(self, priority):
        self._priority = priority

    @property
    def user_id(self):
        return self._user_id
    @user_id.setter
    def user_id(self, user_id):
        self._user_id = user_id

    
    def create(self):
        try:
            db.session.add(self)  # Attempt to add this Task instance to the session
            db.session.commit()  # Commit the session to save changes to the database
            return self  # Return the Task instance if commit was successful
        except IntegrityError:
            db.session.rollback()  # Rollback the session to undo changes in case of an error
            return None  # Return None to indicate the creation failed

    def __str__(self):
        return json.dumps(self.read())  # Convert the output of read() method to JSON string for easy readability

    def create(self):
        try:
            db.session.add(self)  # Attempt to add this Task instance to the session
            db.session.commit()  # Commit the session to save changes to the database
            return self  # Return the Task instance if commit was successful
        except IntegrityError:
            db.session.remove()  # Remove this session due to the integrity error to prevent any residual issues
            return None  # Return None to indicate the creation failed

    def read(self):
        return {
            "id": self.id,  # Return the Task's id
            "title": self.title,  # Return the Task's title
            "description": self.description,  # Return the Task's description
            "priority": self.priority,  # Return the Task's priority
            "user_id": self.user_id  # Return the Task's associated user_id
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, title="", description="", priority="",user_id=0):
        """only updates values with length"""
        if len(title) > 0:
            self.title = title
        if len(description) > 0:
            self.description = description
        if len(priority) > 0:
            self.priority = priority
        if user_id is not None:
            self.user_id = user_id
        db.session.commit()
        return self
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

def initTasks():
    with app.app_context():
        db.create_all()

        t1 = Task(
            title="Dishes",
            description="get the dishes done",
            priority="high",
            user_id=1
        )
        
        t2 = Task(
            title="HW",
            description="finish HW",
            priority="medium",
            user_id=2
        )

        t3 = Task(
            title="Soccer Practice",
            description="practice",
            priority="low",
            user_id=3
        )

        t4 = Task(
            title="Grocery Shopping",
            description="buy groceries for the week",
            priority="medium",
            user_id=4
        )

        t5 = Task(
            title="Call Mom",
            description="catch up call with mom",
            priority="low",
            user_id=5
        )

        tasks = [t1, t2, t3, t4, t5]

        # Add tasks to the session and commit them to the database
        db.session.add_all(tasks)
        db.session.commit()

        # print("-------------------------- USERS -----------------------------")
        # print(users)
        """Builds sample user/note(s) data"""
        # i = 0
        # Attempt to create each task, handling IntegrityError if encountered
        
        for task in tasks:  # Loop through each task in the tasks list
            try:
                task.create()  # Try to create (add and commit) the task to the database
            except IntegrityError:  # Catch any IntegrityError that occurs during task creation
                db.session.remove()  # Remove the current session to clean up any residual state
                print(f"Records exist, duplicate email, or error: {task.id}")  # Print an error message showing which task ID caused the error
