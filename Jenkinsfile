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
                    // Clean up any existing containers and resources
                    sh 'docker-compose -p selenium_pipeline down --volumes --remove-orphans || true'
                    sh 'docker system prune -f || true'
                }
            }
        }
        
        stage('Build and Run Containers') {
            steps {
                dir('app') {
                    echo '🐳 Running docker-compose in app directory...'
                    sh 'docker-compose -p selenium_pipeline up --abort-on-container-exit --build'
                }
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
            // Clean up even if pipeline fails
            dir('app') {
                sh 'docker-compose -p selenium_pipeline down --volumes --remove-orphans || true'
            }
        }
    }
}