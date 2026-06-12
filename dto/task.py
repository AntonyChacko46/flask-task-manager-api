from datetime import date
from dto.user import User
from util.validators import validate_priority,validate_status

class Task:
    """
    Represents a task with their task id, title, description, due date and priority.
    This class is a pure data holder (DTO).
    """
    def __init__(self,task_id:int,title:str,description:str,due_date:date,priority:str, status="TO DO", user_id=None):
        """
        Initializes a new Task instance.

        Args:
            task_id (int): Unique identifier for the task.
            title (str): Title of the task.
            description (str): Detailed description of the task.
            due_date (date): Due date for the task.
            priority (str): Priority level of the task (LOW, MEDIUM, HIGH).

        Returns:
            None

        Raises:
            ValueError: If the priority is invalid.
        """
        self.task_id=task_id
        self.title=title
        self.description=description
        self.assigned_to=user_id
        self.status=status
        validate_priority(priority)
        self.priority = priority
        self.due_date = due_date

    def update_status(self, new_status):
        """
        Updates the task's status after validating it.

        Args:
            new_status (str): The new status to be set (TO DO, IN PROGRESS, DONE).

        Returns:
            None

        Raises:
            ValueError: If the status is invalid.
        """
        while True:
            try:
                new_status=new_status.upper()
                validate_status(new_status)
                self.status = new_status
                break
            except ValueError as e:
                print(e)
                new_status = input("Re-enter a valid status (TO DO, IN PROGRESS, DONE): ")

    def update_priority(self, new_priority):
        """
        Updates the task's priority after validating it.

        Args:
            new_priority (str): The new priority to be set (LOW, MEDIUM, HIGH).

        Returns:
            None

        Raises:
            ValueError: If the priority is invalid.
        """
        while True:
            try:
                new_priority=new_priority.upper()
                validate_priority(new_priority)
                self.priority = new_priority
                break
            except ValueError as e:
                print(e)
                new_priority = input("Re-enter a valid priority (LOW, MEDIUM, HIGH): ")

    def assign_to_user(self,user):
        """
        Assigns the task to a user and updates the user's task list.

        Args:
            user (User): The user to whom the task will be assigned.

        Returns:
            None
        """
        self.assigned_to = user
        user.add_task(self)

    def display_info(self):
        """
        Returns a formatted string containing all task details.

        Args:
            None

        Returns:
            str: A string representation of the task's information.
        """
        assigned_name = f"User ID {self.assigned_to}" if self.assigned_to else "Unassigned"
        return (f"Task ID: {self.task_id}\nTitle: {self.title}\nDescription: {self.description}"
                f"\nAssigned To: {assigned_name}\nStatus: {self.status}\nPriority: {self.priority}"
                f"\nDue Date: {self.due_date}\n")