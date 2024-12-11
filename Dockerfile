FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python -m venv /env

# Activate the virtual environment
ENV PATH="/env/bin:$PATH"

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY . /app
WORKDIR /app

# Expose the default Streamlit port
EXPOSE 8080

# Run the application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port", "8080", "--server.enableCORS", "false"]
