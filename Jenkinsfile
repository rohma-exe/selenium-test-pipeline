pipeline {
    agent any

    environment {
        COMPOSE_FILE = 'docker-compose.yml'
        PROJECT_NAME = 'selenium_pipeline'
    }

    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'master', url: 'https://github.com/rohma-exe/selenium-test-pipeline.git'
            }
        }

        stage('Build and Run Tests') {
            steps {
                sh 'docker-compose -p $PROJECT_NAME up --abort-on-container-exit --build'
            }
        }
    }

    post {
        success {
            echo '✅ Tests passed!'
        }
        failure {
            echo '❌ Tests failed. Check console output.'
        }
        always {
            sh 'docker-compose -p $PROJECT_NAME down'
        }
    }
}
