# Use official Python 3.10
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install minimal requirements
RUN pip install --no-cache-dir -r requirements.txt

# Port 7860 is mandatory for Hugging Face Spaces
EXPOSE 7860

# Production CMD using uvicorn directly
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "7860"]
