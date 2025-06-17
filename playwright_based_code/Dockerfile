# Start from the official Playwright image (includes all dependencies and browsers)
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

# Set the working directory
WORKDIR /app

# Copy your Python requirements (adjust as needed)
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of your application code
COPY . .

# If needed, give Playwright permission to install its dependencies (safe in this base image)
RUN playwright install --with-deps

# Set the command to run your script (change 'app.py' to your main file)
CMD ["python", "app.py"]
