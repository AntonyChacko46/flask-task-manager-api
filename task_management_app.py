import re
from datetime import date
from dto.user import User
from dto.task import Task
from service.task_manager import TaskManager
from util.exceptions import TaskManagerException, TaskNotFoundException, UserNotFoundException,IntegerInputException,ValidationError,ValidationException
from util.db import db_creation, get_connection

def main():
    """
    Main driver function for the Task Manager application.
    
    Args:
        None

    Returns:
        None

    Raises:
        TaskManagerException: For generic task manager errors.
        IntegerInputException: If input for task/user IDs is not a valid integer.
        TaskNotFoundException: If a task with the provided ID does not exist.
        UserNotFoundException: If a user with the provided ID does not exist.

    Features:
        - Create users with integer ID validation.
        - Create tasks with integer ID validation and priority normalization.
        - Assign tasks to users.
        - Update task status and priority.
        - View all tasks.
        - View tasks for each user.
        - View tasks filtered by status.
        - Exit the program.
    """
    db_creation()
    tm=TaskManager()
    userss=[]

    while True:
        print("\n--- Task Manager Menu ---")
        print("1. Create User")
        print("2. Create Task")
        print("3. Assign Task to User")
        print("4. Update Task")
        print("5. View All Tasks")
        print("6. View Tasks for Each User")
        print("7. View Tasks by Status")
        print("8. Exit")

        choice = input("Enter your choice: ")
        try:
            if choice=="1":
                try:
                    #user_id=input("Enter ID of User :")
                    #if not user_id.isdigit():
                    #   raise IntegerInputException("User ID must be a valid integer.")
                    #user_id = int(user_id)
                    uname=input("Enter Name of User :")
                    if not uname:
                        raise ValidationError("Name cannot be empty.", field="uname")
                    if not re.fullmatch(r"[A-Za-z ]+", uname):
                        raise ValidationError("Name must contain only alphabets and spaces.", field="uname")
                    uemail=input("Enter Email of User :")
                    if not uemail:
                        raise ValidationError("Email cannot be empty.", field="uemail")
                    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
                    if not re.fullmatch(email_pattern, uemail):
                        raise ValidationException("Invalid email format.", field="uemail", value=uemail)
                    user_=User(None,uname,uemail)
                    tm.create_user(user_)
                    print("User created successfully...")
                except IntegerInputException as e:
                    print(f"Invalid input: {e}")

            elif choice=="2":
                try:
                    #task_id=input("Enter ID of Task :")
                    #if not task_id.isdigit():
                    #    raise IntegerInputException("Task ID must be a valid integer.")
                    #task_id=int(task_id)
                    title=input("Enter the Title :")
                    if not title:
                        raise ValidationError("Title cannot be empty.", field="title")
                    if not re.fullmatch(r"[A-Za-z ]+", title):
                        raise ValidationError("Title must contain only alphabets and spaces.", field="title")
                    description=input("Enter the Description :")
                    if not description:
                        raise ValidationError("Description cannot be empty.", field="description")
                    if not re.fullmatch(r"[A-Za-z ]+", description):
                        raise ValidationError("Description must contain only alphabets and spaces.", field="description")
                    due_date=input("Enter the Date :")
                    if not due_date:
                        raise ValidationError("Due Date cannot be empty.", field="due_date")
                    priority=input("Enter the Priority (LOW, MEDIUM, HIGH):")
                    if not re.fullmatch(r"[A-Za-z ]+", priority):
                        raise ValidationError("Priority must contain only alphabets and spaces.", field="priority")
                    priority=priority.upper()
                    task_=Task(None,title,description,due_date,priority)
                    tm.create_task(task_)
                    print("Task created successfully...")
                except IntegerInputException as e:
                    print(f"Invalid input: {e}")

            elif choice=="3":
                try:
                    user_id=input("Enter ID of User :")
                    if not user_id.isdigit():
                        raise IntegerInputException("User ID must be a valid integer.")
                    user_id = int(user_id)
                    task_id=input("Enter ID of Task :")
                    if not task_id.isdigit():
                        raise IntegerInputException("Task ID must be a valid integer.")
                    task_id=int(task_id)
                    tm.assign_task_to_user(task_id,user_id)
                    print("Task Assigned successfully...")
                except IntegerInputException as e:
                    print(f"Invalid input: {e}")

            elif choice=="4":
                try:
                    task_id=input("Enter ID of Task :")
                    if not task_id.isdigit():
                        raise IntegerInputException("Task ID must be a valid integer.")
                    task_id=int(task_id)
                    task=tm.get_task(task_id)
                    if task:
                        newst=input("Enter the New Status (TO DO, IN PROGRESS, DONE):")
                        newpt=input("Enter the New Priority (LOW, MEDIUM, HIGH):")
                        newst=newst.upper()
                        newpt=newpt.upper()
                        tm.update_task_status_priority(task_id,newst,newpt)
                        #task.update_status(newst)
                        #1
                        # 1task.update_priority(newpt)
                        print("Task Updated Successfully...")
                    else:
                        print("Task not Found...")
                except IntegerInputException as e:
                    print(f"Invalid input: {e}")

            elif choice=="5":
                print("\n---Tasks---\n")
                for i in tm.list_all_tasks():
                    print(i.display_info())

            elif choice == "6":
                print("\n--- Tasks for Each User ---\n")
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT user_id FROM users")
                user_ids = cursor.fetchall()
                if not user_ids:
                    print("No users found.")
                else:
                    for (user_id,) in user_ids:
                        try:
                            tasks = tm.list_tasks_by_user(user_id)
                            if tasks:
                                print(f"\nTasks for User ID {user_id}:")
                                for task in tasks:
                                    print(task.display_info())
                            else:
                                print(f"\nUser ID {user_id} has no assigned tasks.")
                        except UserNotFoundException as e:
                            print(e)
                cursor.close()
                conn.close()


            elif choice=="7":
                status=input("Enter status (TO DO, IN PROGRESS, DONE): ")
                status=status.upper()
                tasks = tm.list_tasks_by_status(status)
                if tasks:
                    for task in tasks:
                        print(task.display_info())
                else:
                    print("No Tasks are Available with this Status...")

            elif choice=="8":
                print("EXIT!!!")
                break

            else:
                print("Please Enter a Valid Choice...")
        
        except TaskManagerException as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()