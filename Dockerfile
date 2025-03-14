FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY run_model.py .
COPY prompt.json .
COPY .env .

# Set default command
CMD ["python", "run_model.py"]
