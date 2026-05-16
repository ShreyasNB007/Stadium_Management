pipeline {
    agent any

    stages {

        stage('Clone Repository') {
            steps {
                git branch: 'main',
                url: 'git@github.com:YOUR_USERNAME/YOUR_REPO.git'
            }
        }

        stage('Stop Old Containers') {
            steps {
                bat 'docker compose down'
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