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
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.rollback()
            return None

    def __str__(self):
        return json.dumps(self.read())

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def read(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "user_id": self.user_id
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
            title = "e",
            description = "e",
            priority = "e",
            user_id = 1
        )
        
        t2 = Task(
            title = "f",
            description = "f",
            priority = "f",
            user_id = 2
        )

        t3 = Task(
            title = "g",
            description = "g",
            priority = "g",
            user_id = 3
        )

        tasks = [t1, t2, t3]
        # print("-------------------------- USERS -----------------------------")
        # print(users)
        """Builds sample user/note(s) data"""
        # i = 0
        for task in tasks:
            try:
                task.create()
            except IntegrityError:
                """fails with bad or duplicate data"""
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {task.id}")