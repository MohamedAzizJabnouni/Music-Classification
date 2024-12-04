# Use a larger base image for troubleshooting
FROM python:3.9

# Set the working directory
WORKDIR /app

# Install pip and upgrade to the latest version
RUN pip install --upgrade pip

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . /app/

# Expose the Flask port (5000, which is Flask's default)
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]
