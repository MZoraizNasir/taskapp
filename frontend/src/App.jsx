// Import necessary tools
import { useState, useEffect } from 'react';
import axios from 'axios'; // For making HTTP requests
import './App.css'; // Styling

function App() {
  // Set up small memories ("state") to store form inputs and tasks
  const [description, setDescription] = useState('');
  const [assignedTo, setAssignedTo] = useState('');
  const [progress, setProgress] = useState('In Progress');
  const [tasks, setTasks] = useState([]);

  // When the page first loads, fetch the list of tasks
  useEffect(() => {
    fetchTasks();
  }, []);

  // Fetch all tasks from the backend
  const fetchTasks = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/tasks');
      
      setTasks(response.data); // Save the tasks into state
    } catch (error) {
      console.error('Error fetching tasks:', error);
    }
  };

  // Handle submitting the form to add a new task
  const handleSubmit = async (e) => {
  e.preventDefault(); // Prevent page refresh

  const newTask = {
    id: tasks.length + 1, // Generate a temporary ID
    description,
    assigned_to: assignedTo,
    progress,
  };

  try {
    // Attempt to send the new task to the backend
    await axios.post('http://127.0.0.1:5000/tasks', newTask);
    fetchTasks(); // Refresh the task list after adding
  } catch (error) {
    console.error('Error adding task to backend:', error);

    // If backend is not reachable, add the task to the global list
    setTasks((prevTasks) => [...prevTasks, newTask]);
  }

  // Clear the form fields
  setDescription('');
  setAssignedTo('');
  setProgress('In Progress');
};
  // Handle changing progress locally (only in React state)
  const handleLocalProgressChange = (taskId, newProgress) => {
    const updatedTasks = tasks.map((task) => {
      if (task.id === taskId) {
        return { ...task, progress: newProgress };
      }
      return task;
    });
    setTasks(updatedTasks);
  };

  // Handle clicking Update button to save to backend
  const updateTaskProgress = async (taskId, newProgress) => {
    try {
      await axios.put(`http://127.0.0.1:5000/tasks/${taskId}`, {
        progress: newProgress,
      });
      fetchTasks(); // Refresh list after update
      alert("task status updated!");

    } catch (error) {
      console.error('Error updating task progress:', error);
    }
  };
  // Function to delete a task
const deleteTask = async (taskId) => {
  try {
    await axios.delete(`http://127.0.0.1:5000/tasks/${taskId}`);
    fetchTasks(); // Refresh after deleting
  } catch (error) {
    console.error('Error deleting task:', error);
  }
};

  return (
    <div className="container">
      {/* Big title */}
      <h1 className="title">Task Manager App</h1>

      {/* Form to add a new task */}
      <form onSubmit={handleSubmit} className="form">
        <div className="form-group">
          <label>Task Description:</label>
          <input
            type="text"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label>Assign To:</label>
          <select
            value={assignedTo}
            onChange={(e) => setAssignedTo(e.target.value)}
            required
          >
            {/* Empty placeholder */}
            <option value="" disabled>
              Select a name...
            </option>
            <option value="Zoraiz">Zoraiz</option>
            <option value="kian">kian</option>
            <option value="sadhana">sadhana</option>
          </select>
        </div>

        {/* Submit button */}
        <button type="submit" className="submit-btn">
          Add Task
        </button>
      </form>

      {/* Section to display all tasks */}
      <div className="task-list">
        <h2>All Tasks</h2>
        <table>
          <thead>
            <tr>
              <th>Task</th>
              <th>Assigned To</th>
              <th>Progress</th>
            </tr>
          </thead>
          <tbody>
            {tasks.map((task) => (
              <tr key={task.id}>
                <td>{task.description}</td>
                <td>{task.assigned_to}</td>
                <td style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  {/* Progress dropdown */}
                  <select
                    value={task.progress}
                    onChange={(e) => handleLocalProgressChange(task.id, e.target.value)}
                    className="progress-dropdown"
                  >
                    <option value="In Progress">In Progress</option>
                    <option value="Completed">Completed</option>
                    <option value="Cancelled">Cancelled</option>
                  </select>

                  {/* Update Button */}
                  <button
                    className="update-btn"
                    onClick={() => updateTaskProgress(task.id, task.progress)}
                  >
                    Update
                  </button>

                  {/* Delete Button */}
                  <button
                    className="delete-btn"
                    onClick={() => deleteTask(task.id)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;
