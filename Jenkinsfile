pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "sudhakaran97/aceest-fitness"
        APP_VERSION  = "v3.2.4"
        SONAR_HOST   = "http://localhost:9000"
        SONAR_TOKEN  = credentials('sonar-token')
        DOCKER_CREDS = credentials('docker-hub-creds')
        GIT_REPO     = "https://github.com/SudhakaranSekar/aceest-fitness-devops.git"
    }

    stages {

        // ── STAGE 1: Checkout ──────────────────────────────
        stage('Checkout') {
            steps {
                echo '========== Checking out source code =========='
                git branch: 'main', url: "${GIT_REPO}"
            }
        }

        // ── STAGE 2: Install Dependencies ─────────────────
        stage('Install Dependencies') {
            steps {
                echo '========== Installing Python dependencies =========='
                bat 'pip install -r requirements.txt'
                bat 'pip install pytest pytest-flask'
            }
        }

        // ── STAGE 3: Run Pytest ────────────────────────────
        stage('Run Tests') {
            steps {
                echo '========== Running Pytest unit tests =========='
                bat 'pytest test_app.py -v --tb=short'
            }
            post {
                failure {
                    echo 'Tests FAILED! Stopping pipeline.'
                }
                success {
                    echo 'All tests PASSED!'
                }
            }
        }

        // ── STAGE 4: SonarQube Analysis ───────────────────
        stage('SonarQube Analysis') {
            steps {
                echo '========== Running SonarQube code analysis =========='
                bat """
                    sonar-scanner ^
                    -Dsonar.projectKey=aceest-fitness ^
                    -Dsonar.projectName=ACEest-Fitness ^
                    -Dsonar.projectVersion=${APP_VERSION} ^
                    -Dsonar.sources=. ^
                    -Dsonar.python.version=3 ^
                    -Dsonar.host.url=${SONAR_HOST} ^
                    -Dsonar.login=${SONAR_TOKEN}
                """
            }
        }

        // ── STAGE 5: Build Docker Image ───────────────────
        stage('Build Docker Image') {
            steps {
                echo '========== Building Docker image =========='
                bat "docker build -t ${DOCKER_IMAGE}:${APP_VERSION} ."
                bat "docker tag ${DOCKER_IMAGE}:${APP_VERSION} ${DOCKER_IMAGE}:latest"
            }
        }

        // ── STAGE 6: Push to Docker Hub ───────────────────
        stage('Push to Docker Hub') {
            steps {
                echo '========== Pushing image to Docker Hub =========='
                bat "docker login -u ${DOCKER_CREDS_USR} -p ${DOCKER_CREDS_PSW}"
                bat "docker push ${DOCKER_IMAGE}:${APP_VERSION}"
                bat "docker push ${DOCKER_IMAGE}:latest"
            }
        }

        // ── STAGE 7: Deploy to Kubernetes ─────────────────
        stage('Deploy to Kubernetes') {
            steps {
                echo '========== Deploying to Kubernetes (Minikube) =========='
                bat 'minikube status'
                bat 'kubectl apply -f k8s/rolling-update.yaml'
                bat 'kubectl rollout status deployment/aceest-fitness'
            }
        }

        // ── STAGE 8: Verify Deployment ────────────────────
        stage('Verify Deployment') {
            steps {
                echo '========== Verifying deployment health =========='
                bat 'kubectl get pods -l app=aceest-fitness'
                bat 'kubectl get services'
            }
        }
    }

    // ── POST ACTIONS ──────────────────────────────────────
    post {
        success {
            echo """
            ============================================
            PIPELINE SUCCEEDED!
            App Version : ${APP_VERSION}
            Docker Image: ${DOCKER_IMAGE}:${APP_VERSION}
            ============================================
            """
        }
        failure {
            echo """
            ============================================
            PIPELINE FAILED!
            Check the logs above for errors.
            ============================================
            """
        }
        always {
            echo 'Pipeline finished. Cleaning up...'
            bat 'docker logout'
        }
    }
}
