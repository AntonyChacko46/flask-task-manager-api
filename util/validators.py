import re
from util.exceptions import ValidationException

def validate_user_id(user_id):
    """
    Validates that the user_id is a positive integer.

    Args:
        user_id (int): The user ID to validate.

    Returns:
        None

    Raises:
        ValidationException: If user_id is not a positive integer.
    """
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValidationException("User ID must be a positive integer.", field="user_id", value=user_id)

def validate_task_id(task_id):
    """
    Validates that the task_id is a positive integer.

    Args:
        task_id (int): The task ID to validate.

    Returns:
        None

    Raises:
        ValidationException: If task_id is not a positive integer.
    """
    if not isinstance(task_id, int) or task_id <= 0:
        raise ValidationException("Task ID must be a positive integer.", field="task_id", value=task_id)

def validate_string_field(value, field_name):
    """
    Validates that the given value is a non-empty string.

    Args:
        value (str): The value to validate.
        field_name (str): The name of the field being validated.

    Returns:
        None

    Raises:
        ValidationException: If the value is not a non-empty string.
    """
    if not isinstance(value, str) or not value.strip():
        raise ValidationException(f"{field_name.capitalize()} must be a non-empty string.", field=field_name, value=value)

def validate_status(status):
    """
    Validates that the status is one of the allowed values.

    Args:
        status (str): The status to validate. Must be one of ["TO DO", "IN PROGRESS", "DONE"].

    Returns:
        None

    Raises:
        ValidationException: If the status is not valid.
    """
    valid_statuses = ["TO DO", "IN PROGRESS", "DONE"]
    if status not in valid_statuses:
        raise ValidationException("Invalid status.", field="status", value=status)

def validate_priority(priority):
    """
    Validates that the priority is one of the allowed values.

    Args:
        priority (str): The priority to validate. Must be one of ["LOW", "MEDIUM", "HIGH"].

    Returns:
        None

    Raises:
        ValidationException: If the priority is not valid.
    """
    valid_priorities = ["LOW", "MEDIUM", "HIGH"]
    if priority not in valid_priorities:
        raise ValidationException("Invalid priority.", field="priority", value=priority)
    
