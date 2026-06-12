from flask import Blueprint, request, jsonify
from dto.user import User
from service.task_manager import TaskManager
from util.exceptions import ValidationException, DuplicateUserException, UserNotFoundException
import re

user_blueprint = Blueprint("user_controller", __name__, url_prefix="/users")
tm = TaskManager()

@user_blueprint.route("/", methods=["POST"])
def create_user():
    """
    Creates a new user with validated input data (user_id is auto-incremented).

    Args:
        JSON input expected in request body with keys: uname, uemail

    Returns:
        JSON response with success message and inserted user_id (HTTP 201).
        JSON error message (HTTP 400) on validation/duplication errors.

    Raises:
        ValidationException: If name or email is invalid.
        DuplicateUserException: If email already exists.
    """
    try:
        data = request.json
        
        uname = data.get('uname')
        if not uname or not isinstance(uname, str):
            raise ValidationException("Name cannot be empty.", field="uname")
        if not re.fullmatch(r"[A-Za-z ]+", uname):
            raise ValidationException("Name must contain only alphabets and spaces.", field="uname")
        
        uemail = data.get('uemail')
        if not uemail or not isinstance(uemail, str):
            raise ValidationException("Email cannot be empty.", field="uemail")
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.fullmatch(email_pattern, uemail):
            raise ValidationException("Invalid email format.", field="uemail")
        
        user = User(None, uname, uemail)  # ID is auto-generated
        inserted_id = tm.create_user(user)

        return jsonify({"message": "User created successfully.", "user_id": inserted_id}), 201
    except (ValidationException, DuplicateUserException) as e:
        return jsonify({"error": str(e)}), 400


@user_blueprint.route("/<int:user_id>/tasks", methods=["GET"])
def get_user_tasks(user_id):
    """
    Retrieves all tasks assigned to a given user ID.

    Args:
        user_id (int): The user ID from the URL path.

    Returns:
        JSON response with a list of task objects and HTTP 200 status code if successful.
        JSON error message and HTTP 404 if user is not found.
        JSON error message and HTTP 400 if user_id is invalid.

    Raises:
        ValidationException: If the user_id is not a valid positive integer.
        UserNotFoundException: If no user exists with the given user_id.
    """
    try:
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValidationException("User ID must be a positive integer.", field="user_id")

        tasks = tm.list_tasks_by_user(user_id)
        return jsonify([task.__dict__ for task in tasks]), 200
    except UserNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except ValidationException as e:
        return jsonify({"error": str(e)}), 400
