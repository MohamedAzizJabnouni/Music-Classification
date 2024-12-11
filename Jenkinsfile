pipeline {
    agent any

    environment {
        PROJECT_DIR = '/var/jenkins_home/workspace/music-classification'  // Use this variable for reusability
        FRONTEND_IMAGE = 'front_image'
        SVM_IMAGE = 'svm_image'
        VGG19_IMAGE = 'vgg_image'
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
                        sh "docker build -t ${env.FRONTEND_IMAGE} ./Front"
                        sh "docker build -t ${env.SVM_IMAGE} ./SVM"
                        sh "docker build -t ${env.VGG19_IMAGE} ./VGG19"
                    }
                }
            }
        }

        stage('Run Containers') {
            steps {
                script {
                    // Create the Docker network if it doesn't exist
                    sh "docker network inspect app-network || docker network create app-network"

                    // Remove any existing containers with the same names
                    sh "docker ps -a --filter 'name=frontend_container1' --format '{{.ID}}' | xargs -r docker rm -f"
                    sh "docker ps -a --filter 'name=svm_service_container1' --format '{{.ID}}' | xargs -r docker rm -f"
                    sh "docker ps -a --filter 'name=vgg19_service_container1' --format '{{.ID}}' | xargs -r docker rm -f"

                    // Run the containers
                    sh "docker run -d -p 80:80 --name frontend_container1 --network app-network ${env.FRONTEND_IMAGE}"
                    sh "docker run -d -p 5000:5000 --name svm_service_container1 --network app-network ${env.SVM_IMAGE}"
                    sh "docker run -d -p 3000:5000 --name vgg19_service_container1 --network app-network ${env.VGG19_IMAGE}"
                }
            }
        }

        // Uncomment and adapt the tests stage if needed
        // stage('Run Tests') {
        //     steps {
        //         script {
        //             sh "docker exec svm_service_container curl -f http://localhost:5000 || exit 1"
        //             sh "docker exec vgg19_service_container curl -f http://localhost:5000 || exit 1"
        //         }
        //     }
        // }

        // stage('Cleanup') {
        //     steps {
        //         script {
        //             // Stop and remove containers after the job is complete
        //             sh "docker stop frontend_container1 svm_service_container1 vgg19_service_container1"
        //             sh "docker rm frontend_container1 svm_service_container1 vgg19_service_container1"

        //             // Optionally, remove the Docker images
        //             // sh "docker rmi ${env.FRONTEND_IMAGE} ${env.SVM_IMAGE} ${env.VGG19_IMAGE}"
        //         }
        //     }
        // }
    }
}
