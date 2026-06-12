# app.py
from flask import Flask, jsonify
from util.db import db_creation
from service.task_manager import TaskManager
from controllers.user_controller import user_blueprint
from controllers.task_controller import task_blueprint

app = Flask(__name__)
db_creation()  # Ensure DB and tables are created

# Register Blueprints
app.register_blueprint(user_blueprint)
app.register_blueprint(task_blueprint)

# Root route
@app.route("/")
def home():
    """
    Root route that displays available API endpoints and instructions.

    Args:
        None

    Returns:
        JSON response with a menu listing all available routes and how to use them.
        HTTP 200 status code.

    Raises:
        None
    """
    return jsonify({
        "MENU": [
            "Welcome to the Task Manager API",
            "1. Create User              : POST /users",
            "2. Create Task              : POST /tasks",
            "3. Assign Task to User      : PUT /tasks/<task_id>/assign/<user_id>",
            "4. Update Task              : PUT /tasks/<task_id>",
            "5. View All Tasks           : GET /tasks",
            "6. View Tasks for Each User : GET /users/<user_id>/tasks",
            "7. View Tasks by Status     : GET /tasks/status/<status>"
        ],
        "NB": "Use Postman or any REST client to access these endpoints."
    })

# 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    """
    Custom handler for undefined routes (404 errors).

    Args:
        e (Exception): The exception object representing the 404 error.

    Returns:
        JSON response with an error message indicating the endpoint was not found.
        HTTP 404 status code.

    Raises:
        None
    """
    return jsonify({"error": "Endpoint Not Found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
