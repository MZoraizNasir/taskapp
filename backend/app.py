# Import necessary libraries
import os 
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

# Initialize the Flask app
app = Flask(__name__)
CORS(app)  # Allow React frontend to connect without CORS errors

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"),
    database=os.getenv("DB_NAME", "taskapp"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD", "admin")
)

# Create a cursor object to execute SQL queries
cur = conn.cursor()

# Route to get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    cur.execute('SELECT * FROM tasks')  # Get all rows from tasks table
    rows = cur.fetchall()
    tasks = []
    for row in rows:
        tasks.append({
            'id': row[0],
            'description': row[1],
            'assigned_to': row[2],
            'progress': row[3]
        })
    return jsonify(tasks)  # Return tasks as JSON

# Route to add a new task
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()  # Get JSON sent from React

    description = data['description']
    assigned_to = data['assignedTo']
    progress = data['progress']

    # Insert new task into the database
    cur.execute(
        'INSERT INTO tasks (description, assigned_to, progress) VALUES (%s, %s, %s)',
        (description, assigned_to, progress)
    )
    conn.commit()  # Save changes to the database

    return {'message': 'Task added successfully!'}

# Route to update a task's progress
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task_progress(task_id):
    data = request.get_json()
    new_progress = data['progress']

    cur.execute(
        'UPDATE tasks SET progress = %s WHERE id = %s',
        (new_progress, task_id)
    )
    conn.commit()

    return {'message': 'Task progress updated successfully!'}

# Route to delete a task by id
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    cur.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
    conn.commit()
    return {'message': 'Task deleted successfully!'}

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
