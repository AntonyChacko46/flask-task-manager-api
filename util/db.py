import mysql.connector

def db_creation():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root"
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS task_manager")
    cursor.execute("USE task_manager")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            uname VARCHAR(100) NOT NULL,
            uemail VARCHAR(100) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description TEXT,
            due_date DATE,
            priority ENUM('LOW', 'MEDIUM', 'HIGH'),
            status ENUM('TO DO', 'IN PROGRESS', 'DONE') DEFAULT 'TO DO',
            user_id INT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("Connected to DB Successfully...")
    

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="task_manager"
    )