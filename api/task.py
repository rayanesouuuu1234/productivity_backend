# api/task.py
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from auth_middleware import token_required  # Uncomment if you have an authentication middleware
from model.tasks import Task  # Make sure this path is correct
from __init__ import app, db

# Create a Blueprint for the tasks API
tasks_blueprint = Blueprint('tasks_api', __name__)
api = Api(tasks_blueprint)

class TaskResource(Resource):
    # @token_required  # Uncomment if you have an authentication middleware
    def get(self):
        tasks = Task.query.all()  # Retrieve all tasks from the database
        a = [task.read() for task in tasks]
        b = jsonify(a)  # Process the tasks into a list of dictionaries
        return (b)  # Return the JSON representation of the list

    def post(self):
        data = request.get_json()
        
        try:
            task = Task(
                title=data['title'],
                description=data.get('description', ''),
                priority=data['priority'],
                user_id=None  # Ensure you pass the correct user_id
            )
            with app.app_context():
                db.create_all()
                task.create()
            a = task.read()
            print ("sds")
            return jsonify(task.read()), 201
        except Exception as e:
            a = {'error': str(e)}
            return a, 500

# Register the TaskResource with the API
api.add_resource(TaskResource, '/tasks')

# Make sure the Task model has methods like create() and read() implemented correctly
