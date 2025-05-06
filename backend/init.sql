-- Create the tasks table if it doesn't already exist
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    assigned_to TEXT NOT NULL,
    progress TEXT DEFAULT 'In Progress'
);
