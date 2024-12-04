pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_FILE = 'docker-compose.yml'  // Path to your Docker Compose file
    }

    stages {
        stage('Checkout') {
            steps {
                // Pull the latest code from your GitHub repository
                git 'https://github.com/DhimiMohamed/music-classification.git'  // Your public GitHub repository URL
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    // Ensure the correct path is used and build the Docker images for the services (frontend, svm-service, and vgg19-service)
                    dir('C:/Users/dhimi/Desktop/Bureau/docker-compose/music classification') {
                        sh 'docker-compose -f $DOCKER_COMPOSE_FILE build'
                    }
                }
            }
        }

        stage('Run Docker Compose') {
            steps {
                script {
                    // Start the containers using Docker Compose in detached mode
                    dir('C:/Users/dhimi/Desktop/Bureau/docker-compose/music classification') {
                        sh 'docker-compose -f $DOCKER_COMPOSE_FILE up -d'
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Run tests (replace with your actual test commands)
                    sh '''
                        docker exec -t music-genre-classification_svm-service_1 curl -f http://localhost:5000/health
                        docker exec -t music-genre-classification_vgg19-service_1 curl -f http://localhost:5000/health
                    '''
                    // Replace the above curl command with appropriate health checks or actual test scripts
                }
            }
        }

        stage('Cleanup') {
            steps {
                script {
                    // Stop and remove containers after the job is complete
                    dir('C:/Users/dhimi/Desktop/Bureau/docker-compose/music classification') {
                        sh 'docker-compose -f $DOCKER_COMPOSE_FILE down'
                    }
                }
            }
        }
    }
}
