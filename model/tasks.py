from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError

class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, title, description, priority, user_id, completed=False):
        self.title = title
        self.description = description
        self.priority = priority
        self.user_id = user_id
        self.completed = completed

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.rollback()
            return None

    def read(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "user_id": self.user_id,
            "completed": self.completed
        }

    def update(self, title=None, description=None, priority=None, completed=None):
        if title:
            self.title = title
        if description:
            self.description = description
        if priority:
            self.priority = priority
        if completed is not None:
            self.completed = completed
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

def initTasks():
    with app.app_context():
        db.create_all()
        # Example task creation
        task1 = Task(
            title='Finish Project', 
            description="Complete the project by EOD.", 
            priority="High", 
            user_id=1,  # Assuming user with ID 1 exists
            completed=False
        )

        tasks = [task1]

        for task in tasks:
            try:
                task.create()
            except IntegrityError:
                db.session.rollback()
                print(f"Task creation failed: {task.title}")

if __name__ == "__main__":
    with app.app_context():
        initTasks()
