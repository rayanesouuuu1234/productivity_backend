import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
# from auth_middleware import token_required
from model.tasks import Task

task_api = Blueprint('task_api', __name__, url_prefix='/api/task')
api = Api(task_api)

class TaskAPI:
    class _CRUD(Resource):
        # @token_required
        def post(self):
            if request.is_json:
                data = request.get_json()
                task_title = data.get('title')
                task_description = data.get('description')
                task_priority = data.get('priority')
                # Assuming 'user_id' is fetched from authenticated user's session or token
                user_id = data.get('user_id')

                task = Task(
                    title=task_title,
                    description=task_description,
                    priority=task_priority,
                    user_id=user_id
                )

                # Save the task to the database
                saved_task = task.create()  # Assuming you have a create method in your Task model
                
                if saved_task:
                    return jsonify(saved_task.read()), 201
                return {'message': 'Failed to create task'}, 500

            else:
                return {'message': 'Request body must be in JSON format'}, 400

        # @token_required
        def get(self):
            # Retrieve all tasks from the database
            tasks = Task.query.all()
            # Convert tasks to JSON-ready format
            json_ready = [task.read() for task in tasks]
            # Return JSON response
            return jsonify(json_ready)

        # Implement other CRUD operations (PUT, DELETE) as needed

    api.add_resource(_CRUD, '/')
