FROM chetan1111/botasaurus:latest

ENV PYTHONUNBUFFERED=1

# Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN python -m pip install --upgrade pip && \
    python -m pip install -r /tmp/requirements.txt

# Create and switch to app directory
WORKDIR /app

# Copy all source files into container
COPY . .

# Ensure Botasaurus installs its components (you can skip this if already handled)
RUN python run.py install || true

# Expose default Streamlit port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
