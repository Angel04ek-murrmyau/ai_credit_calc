pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'angel04ek/ai_credit_calc'
        KUBE_CONFIG = '/var/lib/jenkins/.kube/config'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Клонирование репозитория...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Сборка Docker образа...'
                sh "docker build -t ${DOCKER_IMAGE}:${GIT_COMMIT} ."
            }
        }

        stage('Push Docker Image') {
            steps {
                echo 'Пуш образа в Docker Hub...'
                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub-credentials', 
                    usernameVariable: 'DOCKER_USER', 
                    passwordVariable: 'DOCKER_PASS')]) {
                    
                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    docker push ${DOCKER_IMAGE}:${GIT_COMMIT}
                    docker tag ${DOCKER_IMAGE}:${GIT_COMMIT} ${DOCKER_IMAGE}:latest
                    docker push ${DOCKER_IMAGE}:latest
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Деплой в Kubernetes...'
                sh """
                KUBECONFIG=${KUBE_CONFIG} kubectl set image deployment/ai-credit-calc \
                    ai-credit-calc=${DOCKER_IMAGE}:${GIT_COMMIT}
                KUBECONFIG=${KUBE_CONFIG} kubectl rollout status deployment/ai-credit-calc --timeout=120s
                """
            }
        }
    }

    post {
        always {
            echo 'Очистка старых образов...'
            sh 'docker image prune -f'
        }
        success {
            echo 'Деплой успешен!'
        }
        failure {
            echo 'Деплой провалился!'
        }
    }
}