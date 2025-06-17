pipeline {
    agent any

    environment {
        APP_DIR = 'app'
    }

    stages {
        stage('Clone App Repo') {
            steps {
                echo '📦 Cloning the DevOps_Deployement repo...'
                sh '''
                    rm -rf $APP_DIR
                    git clone https://github.com/rohma-exe/DevOps_Deployement.git $APP_DIR
                '''
            }
        }

        stage('Build and Run Containers') {
            steps {
                dir(env.APP_DIR) {
                    echo '🐳 Building and running containers...'
                    sh 'docker-compose -p selenium_pipeline up -d --build'
                }
            }
        }

        stage('Wait for App to be Ready') {
            steps {
                echo '⏳ Waiting for frontend to be ready...'
                sh '''
                    for i in {1..30}; do
                        curl -s http://localhost:3000 | grep -q "<title>" && break
                        sleep 2
                    done
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo '🧪 Running Selenium tests...'
                sh '''
                    set -e
                    python3 -m venv venv || true
                    . venv/bin/activate
                    pip install -q selenium
                    python test_login.py
                '''
            }
        }
    }

    post {
        always {
            echo '✅ Pipeline complete (containers left running).'
        }
    }
}
