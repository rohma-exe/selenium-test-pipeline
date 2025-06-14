pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/your-username/selenium-test-pipeline.git'
        DOCKER_IMAGE = 'selenium-pipeline'
    }

    stages {
        stage('Clone Repo') {
            steps {
                git url: "${REPO_URL}", branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Run Selenium Tests') {
            steps {
                sh 'docker run --rm $DOCKER_IMAGE'
            }
        }
    }
}
