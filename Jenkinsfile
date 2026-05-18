pipeline {
    agent any

    stages {

        stage('Clone Repository') {
            steps {
                git branch: 'main',
                url: 'https://github.com/ShreyasNB007/Stadium_Management.git'
            }
        }

        stage('Stop Old Containers') {
            steps {
                bat 'docker compose down --remove-orphans'
                bat 'docker rm -f stadium-mysql stadium-app || exit 0'
            }
        }

        stage('Build Containers') {
            steps {
                bat 'docker compose up --build -d'
            }
        }

        stage('Check Running Containers') {
            steps {
                bat 'docker ps'
            }
        }
    }
}