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
                    echo '🐳 Creating network (if missing) and running containers...'
                    sh 'docker network create selenium_pipeline_default || true'
                    sh 'docker-compose -p selenium_pipeline up -d --build'
                }
            }
        }

        stage('Wait for App to be Ready') {
            steps {
                echo '⏳ Waiting for backend/frontend to be ready...'
                sh '''
                STATUS=1
                for i in {1..30}; do
                curl -s http://localhost:3000 | grep -q "<title>" && STATUS=0 && break
                sleep 2
                done
                exit $STATUS
                '''

            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo '🧪 Running Selenium tests...'
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install selenium
                python test_login.py
                '''
            }
        }

        // Optional: Uncomment if you want to stop containers before post
        // stage('Stop Containers') {
        //     steps {
        //         dir('app') {
        //             echo '🛑 Stopping containers...'
        //             sh 'docker-compose -p selenium_pipeline down --volumes'
        //         }
        //     }
        // }
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
