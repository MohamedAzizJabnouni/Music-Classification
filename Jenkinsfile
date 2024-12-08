pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_FILE = 'docker-compose.yml'  // Path to your Docker Compose file
        PROJECT_DIR = 'C:/Users/dhimi/Desktop/Bureau/web_framework/Flask/music-classification'  // Use this variable for reusability
    }

    stages {
        stage('Checkout') {
            steps {
                // Pull the latest code from your GitHub repository
                git 'https://github.com/DhimiMohamed/music-classification.git'  // Public GitHub repository URL
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    // Navigate to the project directory and build the Docker images
                    dir("${env.PROJECT_DIR}") {
                        sh "docker-compose -f ${env.DOCKER_COMPOSE_FILE} build"
                    }
                }
            }
        }

        stage('Run Docker Compose') {
            steps {
                script {
                    // Start the containers using Docker Compose in detached mode
                    dir("${env.PROJECT_DIR}") {
                        sh "docker-compose -f ${env.DOCKER_COMPOSE_FILE} up -d"
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Run tests by executing commands inside running containers
                    sh '''
                        docker exec music-genre-classification_svm-service_1 curl -f http://localhost:5000 || exit 1
                        docker exec music-genre-classification_vgg19-service_1 curl -f http://localhost:5000 || exit 1
                    '''
                }
            }
        }

        stage('Cleanup') {
            steps {
                script {
                    // Stop and remove containers after the job is complete
                    dir("${env.PROJECT_DIR}") {
                        sh "docker-compose -f ${env.DOCKER_COMPOSE_FILE} down"
                    }
                }
            }
        }
    }
}
