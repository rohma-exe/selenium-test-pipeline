# Use lightweight Python image with Chrome pre-installed
FROM joyzoursky/python-chromedriver:3.9-selenium

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy test files
COPY . .

# Set environment variables for headless Chrome
ENV PYTHONPATH=/app

# Default command to run tests
CMD ["python", "-m", "pytest", "test_login.py", "-v", "--tb=short"]