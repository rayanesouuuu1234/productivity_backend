import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource
from datetime import datetime
from auth_middleware import token_required

from model.tasks import Task

tasks_api = Blueprint('tasks_api', __name__,
                   url_prefix='/api/tasks')

api = Api(tasks_api)

class TaskAPI:        
    class _CRUD(Resource):  
        @token_required
        def post(self, current_user):  # Create method
            body = request.get_json()
            
            # Error checking and validation of body goes here

            # Instantiate a Task object
            task = Task(
                name=body.get('name'), 
                priority=body.get('priority'),
                user_id=current_user.id,  # Assuming each task is linked to a user
                # Include other task fields here
            )
            
            # Save task to database
            saved_task = task.create()  # You need to implement this method in your Task model

            if saved_task:
                return jsonify(saved_task.read()), 201  # read() should be a method that serializes the task data
            return {'message': 'Failed to create task'}, 400

        @token_required
        def get(self, current_user):  # Read Method
            # Assuming you want to retrieve tasks for the logged in user only
            tasks = Task.query.filter_by(user_id=current_user.id).all()
            json_ready = [task.read() for task in tasks]  
            return jsonify(json_ready)

        @token_required
        def delete(self, current_user):  # Delete Method
            task_id = request.args.get('id')  # Assuming the task ID is sent as an argument

            # Error checking for task_id goes here

            task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
            if task is None:
                return {'message': 'Task not found'}, 404
            task.delete()  # You need to implement this method in your Task model
            return {'message': f'Deleted task {task_id}'}, 204

    # Add other endpoints if necessary (e.g., for updating tasks)

    # Register the resources with the API
    api.add_resource(_CRUD, '/')

# Register the blueprint in your Flask app
# app.register_blueprint(tasks_api)
