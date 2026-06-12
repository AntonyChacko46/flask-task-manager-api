from flask import Blueprint, request, jsonify
from dto.task import Task
from service.task_manager import TaskManager
from util.exceptions import ValidationException, DuplicateTaskException, TaskNotFoundException, UserNotFoundException
import re

task_blueprint = Blueprint("task_controller", __name__, url_prefix="/tasks")
tm = TaskManager()

@task_blueprint.route("/", methods=["GET"])
def get_all_tasks():
    """
    Fetch all tasks.

    Returns:
        JSON list of all task objects, HTTP 200
    """
    tasks = tm.list_all_tasks()
    return jsonify([task.__dict__ for task in tasks]), 200

@task_blueprint.route("/", methods=["POST"])
def create_task():
    """
    Create a new task with validated input (task_id is auto-incremented).

    Args:
        JSON payload with: title (str), description (str), due_date (YYYY-MM-DD), priority (str)

    Returns:
        JSON success message, HTTP 201

    Raises:
        ValidationException: If input is invalid (HTTP 400)
    """
    try:
        data = request.json

        title = data.get("title")
        if not title or not isinstance(title, str):
            raise ValidationException("Title cannot be empty.", field="title")
        if not re.fullmatch(r"[A-Za-z ]+", title):
            raise ValidationException("Title must contain only alphabets and spaces.", field="title")

        description = data.get("description")
        if not description or not isinstance(description, str):
            raise ValidationException("Description cannot be empty.", field="description")
        if not re.fullmatch(r"[A-Za-z ]+", description):
            raise ValidationException("Description must contain only alphabets and spaces.", field="description")

        due_date = data.get("due_date")
        if not due_date or not isinstance(due_date, str):
            raise ValidationException("Due date must be a string in 'YYYY-MM-DD' format.", field="due_date")
        date_pattern = r"\d{4}-\d{2}-\d{2}"
        if not re.fullmatch(date_pattern, due_date):
            raise ValidationException("Invalid date format. Use YYYY-MM-DD.", field="due_date")

        priority = data.get("priority", "").upper()
        if priority not in ["LOW", "MEDIUM", "HIGH"]:
            raise ValidationException("Priority must be LOW, MEDIUM, or HIGH.", field="priority")

        # Create Task with task_id=None since it's auto-increment
        task = Task(None, title, description, due_date, priority)
        tm.create_task(task)
        return jsonify({"message": "Task created successfully."}), 201

    except (ValidationException, DuplicateTaskException) as e:
        return jsonify({"error": str(e)}), 400

@task_blueprint.route("/<int:task_id>", methods=["GET"])
def get_task_by_id(task_id):
    """
    Retrieve a task by its ID.

    Args:
        task_id (int): ID of the task to fetch

    Returns:
        JSON task object, HTTP 200

    Raises:
        TaskNotFoundException: If task is not found (HTTP 404)
        ValidationException: If task_id is invalid (HTTP 404)
    """
    try:
        if task_id <= 0:
            raise ValidationException("Task ID must be a positive integer.", field="task_id")
        task = tm.get_task(task_id)
        return jsonify(task.__dict__), 200
    except (TaskNotFoundException, ValidationException) as e:
        return jsonify({"error": str(e)}), 404

@task_blueprint.route("/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """
    Update a task's status and priority.

    Args:
        task_id (int): ID of task to update
        JSON: { status: str, priority: str }

    Returns:
        JSON success message, HTTP 200

    Raises:
        ValidationException: Invalid data (HTTP 400)
        TaskNotFoundException: Task not found (HTTP 400)
    """
    try:
        if task_id <= 0:
            raise ValidationException("Task ID must be a positive integer.", field="task_id")

        data = request.json
        status = data.get("status", "").upper()
        priority = data.get("priority", "").upper()

        if status not in ["TO DO", "IN PROGRESS", "DONE"]:
            raise ValidationException("Invalid status. Choose TO DO, IN PROGRESS, or DONE.", field="status")

        if priority not in ["LOW", "MEDIUM", "HIGH"]:
            raise ValidationException("Invalid priority. Choose LOW, MEDIUM, or HIGH.", field="priority")

        tm.update_task_status_priority(task_id, status, priority)
        return jsonify({"message": "Task updated successfully."}), 200

    except (ValidationException, TaskNotFoundException) as e:
        return jsonify({"error": str(e)}), 400

@task_blueprint.route("/<int:task_id>/assign/<int:user_id>", methods=["PUT"])
def assign_task(task_id, user_id):
    """
    Assign a task to a user.

    Args:
        task_id (int): Task to assign
        user_id (int): User to assign to

    Returns:
        JSON success message, HTTP 200

    Raises:
        TaskNotFoundException, UserNotFoundException, ValidationException (HTTP 400)
    """
    try:
        if task_id <= 0:
            raise ValidationException("Task ID must be a positive integer.", field="task_id")
        if user_id <= 0:
            raise ValidationException("User ID must be a positive integer.", field="user_id")

        tm.assign_task_to_user(task_id, user_id)
        return jsonify({"message": f"Task {task_id} assigned to user {user_id}."}), 200

    except (TaskNotFoundException, UserNotFoundException, ValidationException) as e:
        return jsonify({"error": str(e)}), 400

@task_blueprint.route("/status/<status>", methods=["GET"])
def get_tasks_by_status(status):
    """
    Get all tasks with a specific status.

    Args:
        status (str): TO DO, IN PROGRESS, or DONE

    Returns:
        JSON list of matching tasks, HTTP 200

    Raises:
        ValidationException: Invalid status (HTTP 400)
    """
    try:
        status = status.upper()
        if status not in ["TO DO", "IN PROGRESS", "DONE"]:
            raise ValidationException("Invalid status. Must be TO DO, IN PROGRESS, or DONE.", field="status")

        tasks = tm.list_tasks_by_status(status)
        return jsonify([task.__dict__ for task in tasks]), 200

    except ValidationException as e:
        return jsonify({"error": str(e)}), 400
