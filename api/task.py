# api/task.py
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from auth_middleware import token_required  # Uncomment if you have an authentication middleware
from model.tasks import Task  # Make sure this path is correct
from __init__ import app, db
from model.users import User 
import jwt

# Create a Blueprint for the tasks API
tasks_blueprint = Blueprint('tasks_api', __name__, url_prefix='/api/tasks')
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
            print(task.read())
            return task.read(), 201
        except Exception as e:
            print(e)       
    
    def put(self, task_id):
            data = request.get_json()
            task = Task.query.get(task_id)  # Find the task by ID
            if not task:
                return {'error': 'Task not found'}, 404  # Task not found, return HTTP status code for not found
        
            try:
                # Update task properties based on the provided data
                task.title = data.get('title', task.title)
                task.description = data.get('description', task.description)
                task.priority = data.get('priority', task.priority)
                with app.app_context():
                    db.session.commit()  # Commit the changes to the database
                return task.read(), 200  # Return the updated task details and HTTP status code for OK
            except Exception as e:
                return {'error': str(e)}, 400  # Return the error and HTTP status code for bad request 

# Register the TaskResource with the API
api.add_resource(TaskResource, '/tasks')

# Make sure the Task model has methods like create() and read() implemented correctly
