# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install gunicorn
RUN pip install --no-cache-dir gunicorn

# Copy the rest of the application code
COPY . .

# Expose the application port
EXPOSE 5000

# Use gunicorn to serve the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]