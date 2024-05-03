# api/task.py
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from auth_middleware import token_required  # Uncomment if you have an authentication middleware
from model.tasks import Task  # Make sure this path is correct
from __init__ import app, db
from model.users import User 
import jwt

# Import necessary modules from Flask, Flask-RESTful, and other utilities
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from auth_middleware import token_required  # Import custom authentication middleware (uncomment if used)
from model.tasks import Task  # Import Task model (ensure the path is correct)
from __init__ import app, db
from model.users import User 
import jwt

# Create a Flask Blueprint for the tasks API, setting its name and URL prefix
tasks_blueprint = Blueprint('tasks_api', __name__, url_prefix='/api/tasks')
api = Api(tasks_blueprint)  # Create an API object and attach it to the blueprint

tasks_log = []  # Initialize a list to log task information (not used in this snippet)

# Define a resource class for handling tasks using Flask-RESTful
class TaskResource(Resource):

    def get(self):  # Define the HTTP GET method to fetch all tasks
        tasks = Task.query.all()  # Retrieve all task entries from the database
        a = [task.read() for task in tasks]  # Convert each task object to a readable format
        b = jsonify(a)  # Convert the list of tasks to JSON format
        return (b)  # Return the JSON response

    def post(self):  # Define the HTTP POST method to create a new task
        data = request.get_json()  # Get data from the incoming JSON request
        try:
            task = Task(
                title=data['title'],  # Set the title from the request data
                description=data.get('description', ''),  # Get the description, defaulting to an empty string if not provided
                priority=data['priority'],  # Set the priority from the request data
                user_id=None  # Placeholder for user ID association
            )
            with app.app_context():  # Work within the context of the Flask application
                db.create_all()  # Create all database tables (ensure they exist)
                task.create()  # Save the new task to the database
            a = task.read()  # Read the newly created task entry
            print ("sds")  # Debug print statement (should be removed in production)
            print(task.read())  # Print the task details for debugging
            return task.read(), 201  # Return the task details and HTTP status code 201 (Created)
        except Exception as e:
            print(e)  # Print any exceptions that occur during the process
    
    # def put(self, task_id):
    #         data = request.get_json()
    #         task = Task.query.get(task_id)  # Find the task by ID
    #         if not task:
    #             return {'error': 'Task not found'}, 404  # Task not found, return HTTP status code for not found
        
    #         try:
    #             # Update task properties based on the provided data
    #             task.title = data.get('title', task.title)
    #             task.description = data.get('description', task.description)
    #             task.priority = data.get('priority', task.priority)
    #             with app.app_context():
    #                 db.session.commit()  # Commit the changes to the database
    #             return task.read(), 200  # Return the updated task details and HTTP status code for OK
    #         except Exception as e:
    #             return {'error': str(e)}, 400  # Return the error and HTTP status code for bad request 

# Register the TaskResource with the API
api.add_resource(TaskResource, '/tasks')

# Make sure the Task model has methods like create() and read() implemented correctly
