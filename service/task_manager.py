from datetime import date
from dto.user import User
from dto.task import Task
from util.exceptions import (
    TaskManagerException, DuplicateUserException, DuplicateTaskException,
    TaskNotFoundException, UserNotFoundException
)
from util.validators import validate_status
from util.db import get_connection

class TaskManager:
    """
    Manages users and tasks, allowing creation, retrieval, assignment, 
    and filtering of tasks by user or status.
    """

    def __init__(self):
        self.tasks = {}
        self.users = {}

    def create_user(self, user):
        """
        Adds a new user to the system (auto-increment ID handled by DB).

        Args:
            user (User): The user object (with user_id=None)

        Returns:
            None

        Raises:
            DuplicateUserException: If the email already exists.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT uemail FROM users WHERE uemail = %s", (user.uemail,))
        if cursor.fetchone():
            raise DuplicateUserException(user_id="Email already used")

        cursor.execute("INSERT INTO users (uname, uemail) VALUES (%s, %s)", (user.uname, user.uemail))
        conn.commit()
        cursor.close()
        conn.close()

    def create_task(self, task):
        """
        Adds a new task to the system (auto-increment ID handled by DB).

        Args:
            task (Task): The task object (with task_id=None)

        Returns:
            None

        Raises:
            DuplicateTaskException: (Can be skipped as ID is auto)
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tasks (title, description, due_date, priority, status, user_id)
            VALUES (%s, %s, %s, %s, %s, NULL)
        """, (task.title, task.description, task.due_date, task.priority, task.status))
        conn.commit()
        cursor.close()
        conn.close()

    def get_task(self, task_id):
        """
        Retrieves a task by its ID.

        Args:
            task_id (int)

        Returns:
            Task

        Raises:
            TaskNotFoundException
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if not row:
            raise TaskNotFoundException(task_id=task_id)

        return Task(**row)

    def list_all_tasks(self):
        """
        Lists all tasks in the system.

        Returns:
            list of Task
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tasks")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [Task(**row) for row in rows]

    def list_tasks_by_user(self, user_id):
        """
        Lists all tasks assigned to a specific user.

        Args:
            user_id (int)

        Returns:
            list of Task

        Raises:
            UserNotFoundException
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            raise UserNotFoundException(user_id=user_id)

        cursor.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [Task(**row) for row in rows]

    def list_tasks_by_status(self, status):
        """
        Lists all tasks filtered by status.

        Args:
            status (str)

        Returns:
            list of Task
        """
        validate_status(status)
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tasks WHERE status = %s", (status,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [Task(**row) for row in rows]

    def assign_task_to_user(self, task_id, user_id):
        """
        Assigns a task to a user.

        Args:
            task_id (int), user_id (int)

        Raises:
            TaskNotFoundException, UserNotFoundException
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT task_id FROM tasks WHERE task_id = %s", (task_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            raise TaskNotFoundException(task_id=task_id)

        cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            raise UserNotFoundException(user_id=user_id)

        cursor.execute("UPDATE tasks SET user_id = %s WHERE task_id = %s", (user_id, task_id))
        conn.commit()
        cursor.close()
        conn.close()

    def update_task_status_priority(self, task_id: int, status: str, priority: str):
        """
        Updates status and priority of a task.

        Args:
            task_id (int), status (str), priority (str)

        Raises:
            TaskNotFoundException
        """
        validate_status(status)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT task_id FROM tasks WHERE task_id = %s", (task_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            raise TaskNotFoundException(task_id=task_id)

        cursor.execute("""
            UPDATE tasks
            SET status = %s, priority = %s
            WHERE task_id = %s
        """, (status, priority, task_id))
        conn.commit()
        cursor.close()
        conn.close()
