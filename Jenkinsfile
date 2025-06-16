pipeline {
    agent any

    environment {
        IMAGE_NAME = 'selenium-tests'
        REPO_URL = 'https://github.com/rohma-exe/selenium-test-pipeline.git'
    }

    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'master', url: "${REPO_URL}"
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Run Tests in Container') {
            steps {
                sh 'docker run --rm --network host $IMAGE_NAME'
            }
        }
    }

    post {
        success {
            echo "✅ All tests passed."
        }
        failure {
            echo "❌ Tests failed. Check console output."
        }
    }
}
