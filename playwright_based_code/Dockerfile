# Base image with Playwright + Python + Browsers
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

# Avoid Python output buffering
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy Python dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install Playwright dependencies (optional here, but safe)
#RUN playwright install --with-deps
RUN playwright install

# Expose Streamlit default port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

