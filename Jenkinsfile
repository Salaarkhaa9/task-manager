pipeline {
    agent any

    environment {
        WEB_IMAGE_NAME = "my-web-app:${env.BUILD_ID}"
        SELENIUM_IMAGE_NAME = "my-selenium-tests:${env.BUILD_ID}"
        WEB_CONTAINER_NAME = "web-app-${env.BUILD_ID}"
        APP_PORT = "5000"
    }

    stages {
        stage('Code Build') {
            steps {
                echo 'Building Docker image for Web App...'
                sh "docker build -t ${WEB_IMAGE_NAME} ."
                
                echo 'Building Docker image for Selenium tests...'
                dir('selenium_tests') {
                    sh "docker build -f Dockerfile.selenium -t ${SELENIUM_IMAGE_NAME} ."
                }
            }
        }

        stage('Unit Testing') {
            steps {
                echo 'Running unit tests...'
                sh "docker run --rm ${WEB_IMAGE_NAME} pytest test_app.py -v"
            }
        }

        stage('Containerized Deployment') {
            steps {
                echo 'Deploying Web App container...'
                sh """
                    docker network create my-network-${BUILD_ID} || true
                    docker run -d --name ${WEB_CONTAINER_NAME} \
                        --network my-network-${BUILD_ID} \
                        -p ${APP_PORT}:5000 \
                        ${WEB_IMAGE_NAME}
                """
                sh 'sleep 5'
            }
        }

        stage('Containerized Selenium Testing') {
            steps {
                echo 'Running Selenium tests in Docker container...'
                sh """
                    docker run --rm \
                        --network my-network-${BUILD_ID} \
                        -e APP_URL=http://${WEB_CONTAINER_NAME}:5000 \
                        ${SELENIUM_IMAGE_NAME}
                """
            }
        }
    }

    post {
        always {
            echo 'Cleaning up Docker containers and images...'
            sh """
                docker stop ${WEB_CONTAINER_NAME} || true
                docker rm ${WEB_CONTAINER_NAME} || true
                docker network rm my-network-${BUILD_ID} || true
                docker rmi ${WEB_IMAGE_NAME} || true
                docker rmi ${SELENIUM_IMAGE_NAME} || true
            """
        }
    }
}
