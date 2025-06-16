pipeline {
    agent any

    stages {
        stage('Clone App Repo') {
            steps {
                echo '📦 Cloning the DevOps_Deployement repo...'
                sh 'rm -rf app'
                sh 'git clone https://github.com/rohma-exe/DevOps_Deployement.git app'
            }
        }

        stage('Cleanup Docker') {
            steps {
                dir('app') {
                    echo '🧹 Cleaning up existing Docker resources...'
                    sh 'docker-compose -p selenium_pipeline down --volumes --remove-orphans || true'
                    sh 'docker system prune -f || true'
                }
            }
        }

        stage('Build and Run Containers') {
            steps {
                dir('app') {
                    echo '🐳 Running docker-compose in detached mode...'
                    sh 'docker-compose -p selenium_pipeline up -d --build'
                }
            }
        }

        stage('Wait for App to be Ready') {
            steps {
                echo '⏳ Waiting for backend/frontend to be ready...'
                sh 'sleep 15'
            }
        }

        // Optional: add Selenium testing stage here if needed
        stage('Run Selenium Tests') {
            steps {
                echo '🧪 Running Selenium tests...'
                sh 'python3 test_login.py'
            }
        }

        stage('Stop Containers') {
            steps {
                dir('app') {
                    echo '🛑 Stopping containers...'
                    sh 'docker-compose -p selenium_pipeline down --volumes'
                }
            }
        }
    }

    post {
        always {
            echo '✅ Pipeline complete.'
            dir('app') {
                sh 'docker-compose -p selenium_pipeline down --volumes --remove-orphans || true'
            }
        }
    }
}
