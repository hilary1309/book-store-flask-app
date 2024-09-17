# Use the official Python image.
FROM python:3.9

# Set the working directory.
WORKDIR /app

# Copy requirements and install dependencies.
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application code.
COPY . .

# Set environment variables and run the Flask app.
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host=0.0.0.0"]

# Expose the port the app runs on.
EXPOSE 5000
