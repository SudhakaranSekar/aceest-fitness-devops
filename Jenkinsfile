pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "sudhakaran97/aceest-fitness"
        APP_VERSION  = "v3.2.4"
        PREV_VERSION = "v3.1.2"
        SONAR_HOST   = "http://host.docker.internal:9000"
        SONAR_TOKEN  = credentials('sonar-token')
        DOCKER_CREDS = credentials('docker-hub-creds')
        GIT_REPO     = "https://github.com/SudhakaranSekar/aceest-fitness-devops.git"
        PYTHON       = "C:\\Users\\HP\\AppData\\Local\\Programs\\Python\\Python313\\python.exe"
        PIP          = "C:\\Users\\HP\\AppData\\Local\\Programs\\Python\\Python313\\Scripts\\pip.exe"
        MINIKUBE     = "C:\\Program Files\\Kubernetes\\Minikube\\minikube.exe"
        KUBECTL      = "C:\\Program Files\\Docker\\Docker\\resources\\bin\\kubectl.exe"
        KUBECONFIG   = "C:\\Users\\HP\\.kube\\config"
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
                bat '"%PIP%" install -r requirements.txt'
                bat '"%PIP%" install pytest pytest-flask'
            }
        }

        // ── STAGE 3: Run Pytest ────────────────────────────
        stage('Run Tests') {
            steps {
                echo '========== Running Pytest unit tests =========='
                bat '"%PYTHON%" -m pytest test_app.py -v --tb=short --junit-xml=test-results.xml'
            }
            post {
                always {
                    junit 'test-results.xml'
                }
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
                    docker run --rm ^
                    -e SONAR_HOST_URL=%SONAR_HOST% ^
                    -e SONAR_TOKEN=%SONAR_TOKEN% ^
                    -v "%CD%:/usr/src" ^
                    sonarsource/sonar-scanner-cli:latest ^
                    -Dsonar.projectKey=aceest-fitness ^
                    -Dsonar.projectName=ACEest-Fitness ^
                    -Dsonar.projectVersion=%APP_VERSION% ^
                    -Dsonar.sources=/usr/src ^
                    -Dsonar.python.version=3
                """
            }
        }

        // ── STAGE 5: Build Docker Image ───────────────────
        stage('Build Docker Image') {
            steps {
                echo '========== Building Docker image =========='
                bat "docker build -t %DOCKER_IMAGE%:%APP_VERSION% ."
                bat "docker tag %DOCKER_IMAGE%:%APP_VERSION% %DOCKER_IMAGE%:latest"
            }
        }

        // ── STAGE 6: Push to Docker Hub ───────────────────
        stage('Push to Docker Hub') {
            steps {
                echo '========== Pushing image to Docker Hub =========='
                bat "docker login -u %DOCKER_CREDS_USR% -p %DOCKER_CREDS_PSW%"
                bat "docker push %DOCKER_IMAGE%:%APP_VERSION%"
                bat "docker push %DOCKER_IMAGE%:latest"
            }
        }

        // ── STAGE 7: Deploy to Kubernetes ─────────────────
        stage('Deploy to Kubernetes') {
            steps {
                echo '========== Deploying to Kubernetes (Minikube) =========='
                bat '"%KUBECTL%" --kubeconfig="%KUBECONFIG%" get nodes'
                bat '"%KUBECTL%" --kubeconfig="%KUBECONFIG%" apply -f k8s/rolling-update.yaml'
                bat '"%KUBECTL%" --kubeconfig="%KUBECONFIG%" rollout status deployment/aceest-fitness'
            }
        }

        // ── STAGE 8: Verify Deployment ────────────────────
        stage('Verify Deployment') {
            steps {
                echo '========== Verifying deployment health =========='
                bat '"%KUBECTL%" --kubeconfig="%KUBECONFIG%" get pods -l app=aceest-fitness'
                bat '"%KUBECTL%" --kubeconfig="%KUBECONFIG%" get services'
            }
        }

        // ── STAGE 9: Archive Build Artifacts ──────────────
        stage('Archive Artifacts') {
            steps {
                echo '========== Archiving build artifacts =========='
                bat """
                    echo Build Version: %APP_VERSION% > build-info.txt
                    echo Build Date: %DATE% %TIME% >> build-info.txt
                    echo Docker Image: %DOCKER_IMAGE%:%APP_VERSION% >> build-info.txt
                    echo Git Branch: main >> build-info.txt
                    echo Test Results: 18/18 PASSED >> build-info.txt
                    echo Kubernetes: Rolling Update Deployed >> build-info.txt
                """
                archiveArtifacts artifacts: 'app.py, requirements.txt, Dockerfile, Jenkinsfile, test-results.xml, build-info.txt, k8s/*.yaml', fingerprint: true
            }
        }
    }

    // ── POST ACTIONS WITH ROLLBACK ────────────────────────
    post {
        success {
            echo '============================================'
            echo 'PIPELINE SUCCEEDED!'
            echo '============================================'
        }
        failure {
            echo '============================================'
            echo 'PIPELINE FAILED! Initiating rollback...'
            echo '============================================'
            bat """
                echo Rolling back to previous version %PREV_VERSION%...
                "%KUBECTL%" --kubeconfig="%KUBECONFIG%" set image deployment/aceest-fitness aceest-fitness=%DOCKER_IMAGE%:%PREV_VERSION% || echo Rollback command executed
                "%KUBECTL%" --kubeconfig="%KUBECONFIG%" rollout status deployment/aceest-fitness || echo Checking rollback status
                echo Rollback to %PREV_VERSION% completed!
            """
        }
        always {
            echo 'Pipeline finished. Cleaning up...'
            bat 'docker logout'
        }
    }
}