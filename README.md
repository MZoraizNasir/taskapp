**Task Manager Web App - Final Architecture and Setup Guide**

---

# 1. Overview of Architecture

This is a simple **full-stack web application** that allows users to manage a list of tasks.
It is made of two separate parts:

- **Frontend:** Built using **React.js** (with Vite for fast setup).
- **Backend:** Built using **Flask** (Python framework).
- **Database:** **PostgreSQL** to store task information.

The frontend and backend are completely separate projects. They communicate with each other through **HTTP API requests** (REST APIs).

**Data Flow:**
- React app sends data to Flask backend.
- Flask saves, updates, fetches, and deletes data from the PostgreSQL database.
- React displays the updated information.

---

# 2. File Structure

```plaintext
project-folder/
├── frontend/          # React App (Vite project)
│   ├── src/
│   │   ├── App.jsx    # Main frontend logic (UI + API calls)
│   │   ├── App.css    # Frontend styling (CSS)
│   │   └── main.jsx   # React entry point
│   ├── index.html
│   └── package.json
├── backend/           # Flask Backend
│   ├── venv/          # Python virtual environment (dependencies)
│   └── app.py         # Main Flask server file
└── README.md          # (optional) Project instructions
```

---

# 3. Technology Stack

| Layer         | Technology             | Purpose |
|---------------|-------------------------|---------|
| Frontend      | React.js (with Vite)     | Building user interface |
| HTTP Client   | Axios                   | Making API calls from frontend |
| Backend       | Flask (Python)           | Handling APIs and server logic |
| Database      | PostgreSQL               | Storing tasks persistently |
| Other Tools   | flask-cors, psycopg2-binary | CORS handling + Postgres connection |


---

# 4. How to Set Up and Run Locally (VS Code)

## 4.1. Install Required Software
- Install **Node.js** (latest LTS version)
- Install **Python** (3.9+ recommended)
- Install **PostgreSQL** database
- Install **VS Code** (if not already installed)


## 4.2. Backend Setup (Flask)

1. Open VS Code.
2. Open terminal and navigate to your project folder:

```bash
cd backend
```

3. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate   # Windows
# or
source venv/bin/activate # Mac/Linux
```

4. Install Python packages:
```bash
pip install Flask flask-cors psycopg2-binary
```

5. Create `app.py` and add the backend server code.
6. Make sure PostgreSQL is running, and your database and table are set up:
   - Create a `taskapp` database.
   - Create a `tasks` table with columns: `id`, `description`, `assigned_to`, `progress`.
7. Run Flask server:
```bash
python app.py
```

Backend will be available at:
```plaintext
http://127.0.0.1:5000
```


## 4.3. Frontend Setup (React)

1. Open a new terminal tab or window.
2. Navigate to your frontend folder:

```bash
cd frontend
```

3. Install frontend dependencies:
```bash
npm install
```

4. Install Axios:
```bash
npm install axios
```

5. Start the frontend development server:
```bash
npm run dev
```

Frontend will be available at:
```plaintext
http://localhost:5173
```


## 4.4. How They Work Together
- React frontend will send `GET`, `POST`, `PUT`, and `DELETE` API requests to Flask backend.
- Flask backend will interact with PostgreSQL to store, update, retrieve, and delete tasks.
- React will dynamically display the tasks and refresh the list after every change.


---


testing git 