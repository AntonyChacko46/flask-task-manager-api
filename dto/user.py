class User:
    """
    Represents a user with their user id, name and email.
    This class is a pure data holder (DTO).
    """
    def __init__(self,user_id:int,uname:str,uemail:str):
        """
        Initializes a new User instance.

        Args:
            user_id (int): The unique identifier for the user.
            name (str): The name of the user.
            email (str): The email address of the user.

        Returns:
            None
        """
        self.user_id=user_id
        self.uname=uname
        self.uemail=uemail
        self.task_list=[]

    def add_task(self,task):
        """
        Adds a task to the user's task list if it is not already present.

        Args:
            task (Task): The task to be added.

        Returns:
            None
        """
        if task not in self.task_list:
            self.task_list.append(task)

    def remove_task(self,task_id):
        """
        Removes a task from the user's task list by its ID.

        Args:
            task_id (int): The ID of the task to remove.

        Returns:
            None
        """
        self.task_list = [t for t in self.task_list if t.task_id != task_id]

    def view_tasks_by_status(self,status):
        """
        Returns a list of tasks filtered by a specific status.

        Args:
            status (str): The status to filter tasks by (e.g., 'pending', 'completed').

        Returns:
            list: A list of tasks matching the specified status.
        """
        return [t for t in self.task_list if t.status == status]