pipeline {
    agent any

    environment {
        TEST_IMAGE = 'selenium-test-image'
    }

    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'master', url: 'https://github.com/rohma-exe/selenium-test-pipeline.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${TEST_IMAGE} .'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'docker run --rm --network host ${TEST_IMAGE}'
            }
        }
    }
}
