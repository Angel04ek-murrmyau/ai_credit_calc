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

        stage('Check docker access') {
            steps {
                sh 'groups'
                sh 'whoami'
                sh 'docker ps'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Сборка Docker образа с пробросом токена GigaChat...'
                withCredentials([string(credentialsId: 'gigachat-api-key', variable: 'GIGA_SECRET')]) {
                    sh "docker build --build-arg GIGACHAT_CRED_ARG=${GIGA_SECRET} -t ${DOCKER_IMAGE}:${GIT_COMMIT} ."
                }
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
    }

    post {
        always {
            echo 'Очистка старых образов...'
            sh 'docker image prune -f'
        }
        success {
            echo 'Сборка и пуш успешны!'
        }
        failure {
            echo 'Что-то пошло не так...'
        }
    }
}