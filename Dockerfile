# Use Python 3.10.13
FROM python:3.10.13

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Start your Flask app
CMD ["python", "app.py"]
