pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/rohma-exe/DevOps_Deployement.git'
        FOLDER = 'app'
    }

    stages {
        stage('Clone App Repo') {
            steps {
                echo '📦 Cloning the DevOps_Deployement repo...'
                sh 'rm -rf $FOLDER'
                sh 'git clone $REPO_URL $FOLDER'
            }
        }

        stage('Build and Run Containers') {
            steps {
                dir("$FOLDER") {
                    echo '🐳 Running docker-compose in app directory...'
                    sh 'docker-compose -p selenium_pipeline up --abort-on-container-exit --build'
                }
            }
        }

        stage('Stop Containers') {
            steps {
                dir("$FOLDER") {
                    echo '🧹 Cleaning up containers...'
                    sh 'docker-compose -p selenium_pipeline down'
                }
            }
        }
    }

    post {
        always {
            echo '✅ Pipeline complete.'
        }
    }
}
