class TaskManagerException(Exception):
    """
    Base class for all custom exceptions in the Task Manager system.

    Args:
        None

    Returns:
        None

    Raises:
        None
    """
    pass

class TaskNotFoundException(TaskManagerException):
    """
    Raised when a task with the specified ID is not found.

    Args:
        task_id (int, optional): ID of the missing task.

    Returns:
        None

    Raises:
        None
    """
    def __init__(self, task_id=None):
        super().__init__(f"Task with ID {task_id} not found.")

class UserNotFoundException(TaskManagerException):
    """
    Raised when a user with the specified ID is not found.

    Args:
        user_id (int, optional): ID of the missing user.

    Returns:
        None

    Raises:
        None
    """
    def __init__(self, user_id=None):
        super().__init__(f"User with ID {user_id} not found.")

class InvalidInputException(TaskManagerException):
    """
    Raised when input provided by the user is invalid or cannot be processed.

    Args:
        message (str): Description of the error.
        original_exception (Exception, optional): The original exception that caused this error.

    Returns:
        None

    Raises:
        None
    """
    def __init__(self, message="Invalid input provided.", original_exception=None):
        super().__init__(message)
        self.original_exception = original_exception

class ValidationException(TaskManagerException):
    """
    Raised when a value fails custom validation rules.

    Args:
        message (str): Description of the validation failure.
        field (str, optional): The name of the field that failed validation.
        value (any, optional): The invalid value provided.

    Returns:
        None

    Raises:
        None
    """
    def __init__(self, message="Validation failed.", field=None, value=None):
        super().__init__(message)
        self.field = field
        self.value = value

class DuplicateUserException(TaskManagerException):
    """
    Raised when a user with the same ID already exists in the system.

    Args:
        user_id (int): ID of the duplicate user.

    Returns:
        None

    Raises:
        None
    """
    def __init__(self, user_id):
        super().__init__(f"User with ID {user_id} already exists.")

class DuplicateTaskException(TaskManagerException):
    """
    Raised when a task with the same ID already exists in the system.

    Args:
        task_id (int): ID of the duplicate task.

    Returns:
        None

    Raises:
        None
    """
    def __init__(self, task_id):
        super().__init__(f"Task with ID {task_id} already exists.")

class IntegerInputException(Exception):
    """
    Raised when a non-integer value is provided where an integer is required.

    Args:
        message (str): Description of the input error.

    Returns:
        None

    Raises:
        None
    """
    def __init__(self, message="Input must be a valid integer."):
        super().__init__(message)
        
class ValidationError(TaskManagerException):
    """
    Raised when data fails specific validation rules.
    
    Attributes:
        message,Explanation of the validation failure.
        field, The field that failed validation.
        value ,The invalid value provided.
    """
    def __init__(self, message="Validation failed.", field=None, value=None):
        super().__init__(message)
        self.field = field
        self.value = value