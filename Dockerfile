FROM python:3.10-slim

# Install Chrome
RUN apt-get update && apt-get install -y \
    wget unzip gnupg curl \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt install -y ./google-chrome*.deb \
    && rm google-chrome*.deb

# Install ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') && \
    CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE") && \
    wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver.zip

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy test files
COPY . /app
WORKDIR /app

# Run tests
CMD ["python", "test_login.py"]
