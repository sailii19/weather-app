
pipeline {
    agent none

    environment {
        AWS_REGION = 'ap-south-1'
        AWS_ACCOUNT_ID = '658860694090'
        ECR_REPOSITORY = 'image-regi'
        IMAGE_NAME = 'cloud-image'
        ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        ECR_IMAGE = "${ECR_REGISTRY}/${ECR_REPOSITORY}:latest"
    }

    stages {
        stage('Build and Push to ECR') {
            agent { label 'built-in' }

            stages {
                stage('Checkout') {
                    steps {
                        checkout scm
                    }
                }

                stage('Build and Test') {
                    steps {
                        sh 'python3 -m venv .venv'
                        sh '.venv/bin/pip install -r requirements.txt'
                        sh '.venv/bin/python -m py_compile app.py'
                    }
                }

                stage('Docker Build') {
                    steps {
                        sh 'docker build -t ${IMAGE_NAME}:latest .'
                    }
                }

                stage('ECR Login') {
                    steps {
                        sh '''
                            aws ecr get-login-password --region ${AWS_REGION} |
                            docker login --username AWS --password-stdin ${ECR_REGISTRY}
                        '''
                    }
                }

                stage('Docker Tag') {
                    steps {
                        sh 'docker tag ${IMAGE_NAME}:latest ${ECR_IMAGE}'
                    }
                }

                stage('Push to ECR') {
                    steps {
                        sh 'docker push ${ECR_IMAGE}'
                    }
                }
            }
        }

        stage('Deploy to Minikube') {
            agent { label 'minikube-local' }

            steps {
                checkout scm

                bat '''
                    minikube kubectl -- apply -f k8s/
                    minikube kubectl -- rollout restart deployment/weather-app
                    minikube kubectl -- rollout status deployment/weather-app --timeout=180s
                '''
            }
        }

        stage('Verify Deployment') {
            agent { label 'minikube-local' }

            steps {
                bat 'minikube kubectl -- get deployments weather-app'
                bat 'minikube kubectl -- get services weather-service'
                bat 'minikube kubectl -- get pods -l app=weather-app'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
