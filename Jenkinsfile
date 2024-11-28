pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "wajdi.bejaouui/django-app"
        DOCKER_TAG = "latest" // Or dynamically set with BUILD_NUMBER or GIT_COMMIT
    }

    stages {
        stage('Build') {
            steps {
                script {
                    // Build the Docker image
                    sh '''
                    echo "Building Docker Images with Docker Compose"
                    docker-compose build
                    '''
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    script {
                        // Push the image to Docker Hub
                        sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                        '''
                    }
                }
            }
        }
    }
}
