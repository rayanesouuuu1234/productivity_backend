from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from sqlalchemy.exc import IntegrityError

from __init__ import db, app
from auth_middleware import token_required  # Make sure you have this middleware for authentication

# Database Model
class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(50), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Assuming the User model is defined elsewhere

    def __init__(self, title, description, priority, user_id):
        self.title = title
        self.description = description
        self.priority = priority
        self.user_id = user_id

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def read(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "completed": self.completed,
            "user_id": self.user_id
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

# Flask-Restful setup
tasks_api = Blueprint('tasks_api', __name__, url_prefix='/api/tasks')
api = Api(tasks_api)

# Task Resource
class TaskResource(Resource):
    @token_required
    def get(self, current_user):  # Read all tasks for current user
        tasks = Task.query.filter_by(user_id=current_user.id).all()
        return jsonify([task.read() for task in tasks])

    @token_required
    def post(self, current_user):  # Create a new task
        body = request.get_json()
        task = Task(
            title=body.get('title'),
            description=body.get('description'),
            priority=body.get('priority'),
            user_id=current_user.id
        )
        try:
            task.create()
            return jsonify(task.read()), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({"message": "Could not create task."}), 400

    @token_required
    def put(self, current_user):  # Update an existing task
        body = request.get_json()
        task_id = body.get('id')
        task = Task.query.get(task_id)
        
        if task and task.user_id == current_user.id:
            task.update(
                title=body.get('title'),
                description=body.get('description'),
                priority=body.get('priority'),
                completed=body.get('completed')
            )
            return jsonify(task.read()), 200
        return jsonify({"message": "Task not found or unauthorized"}), 404

    @token_required
    def delete(self, current_user):  # Delete a task
        task_id = request.args.get('id')
        task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
        
        if task:
            task.delete()
            return jsonify({"message": "Task deleted"}), 204
        return jsonify({"message": "Task not found"}), 404

# Register the resource
api.add_resource(TaskResource, '/')

# Make sure to initialize your database and create tables as needed
# Ensure you have a User model that the Task model can reference
# Make sure to include authentication middleware that handles @token_required