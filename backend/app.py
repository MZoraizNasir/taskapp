import os
import logging
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import psycopg2

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# Initialize the Flask app
app = Flask(__name__)
CORS(app)

# Connect to PostgreSQL database
try:
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "taskapp"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "admin")
    )
    cur = conn.cursor()
    logging.info("Database connection established.")
except Exception as e:
    logging.error("Error connecting to the database.", exc_info=True)

# Homepage route
@app.route('/', methods=['GET'])
def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head><title>Task Manager API</title></head>
    <body>
        <h2>Welcome to the Task Manager API</h2>
        <p>Use the <code>/tasks</code> endpoint to view or manage tasks.</p>
    </body>
    </html>
    """
    return render_template_string(html)

# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        logging.info("GET /tasks request received.")
        cur.execute('SELECT * FROM tasks')
        rows = cur.fetchall()
        tasks = [{
            'id': row[0],
            'description': row[1],
            'assigned_to': row[2],
            'progress': row[3]
        } for row in rows]
        logging.info("Returning %d tasks.", len(tasks))
        return jsonify(tasks)
    except Exception as e:
        logging.error("Error fetching tasks.", exc_info=True)
        return jsonify({'error': 'Failed to fetch tasks'}), 500

# Add a new task
@app.route('/tasks', methods=['POST'])
def add_task():
    try:
        logging.info("POST /tasks request received.")
        data = request.get_json()
        logging.info("Payload: %s", data)

        description = data['description']
        assigned_to = data['assignedTo']
        progress = data['progress']

        cur.execute(
            'INSERT INTO tasks (description, assigned_to, progress) VALUES (%s, %s, %s)',
            (description, assigned_to, progress)
        )
        conn.commit()
        logging.info("Task added successfully.")
        return {'message': 'Task added successfully!'}
    except Exception as e:
        logging.error("Error adding task.", exc_info=True)
        return jsonify({'error': 'Failed to add task'}), 500

# Update task progress
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task_progress(task_id):
    try:
        logging.info("PUT /tasks/%d request received.", task_id)
        data = request.get_json()
        new_progress = data['progress']
        logging.info("Updating task %d progress to %s.", task_id, new_progress)

        cur.execute(
            'UPDATE tasks SET progress = %s WHERE id = %s',
            (new_progress, task_id)
        )
        conn.commit()
        logging.info("Task progress updated.")
        return {'message': 'Task progress updated successfully!'}
    except Exception as e:
        logging.error("Error updating task.", exc_info=True)
        return jsonify({'error': 'Failed to update task'}), 500

# Delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        logging.info("DELETE /tasks/%d request received.", task_id)
        cur.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
        conn.commit()
        logging.info("Task deleted.")
        return {'message': 'Task deleted successfully!'}
    except Exception as e:
        logging.error("Error deleting task.", exc_info=True)
        return jsonify({'error': 'Failed to delete task'}), 500

# Run the app
if __name__ == '__main__':
    port = int(os.getenv("APP_PORT", 5000))
    logging.info("Starting Flask server on port %d", port)
    app.run(host='0.0.0.0', port=port, debug=False)
