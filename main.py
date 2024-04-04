import threading
from flask import render_template, request
from flask.cli import AppGroup

from __init__ import app, db  # cors import removed if not used

# Import API Blueprints
from api.task import tasks_api
from model.tasks import init_db

# Setup app pages if you have any, otherwise, remove this
from projects.projects import app_projects

# Initialize the SQLAlchemy object with the Flask app
db.init_app(app)

# Register API routes
app.register_blueprint(tasks_api)

# Register app pages - only if you have this setup
app.register_blueprint(app_projects)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/table/')
def table():
    return render_template("table.html")

# Create an AppGroup for custom commands
custom_cli = AppGroup('custom', help='Custom commands')

@custom_cli.command('generate_data')
def generate_data():
    init_db()  # Assumes init_db will setup initial data for tasks and possibly users

# Register the custom command group with the Flask app
app.cli.add_command(custom_cli)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8086")
