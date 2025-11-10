pipeline {
    agent any
    
    environment {
        // Docker Hub credentials (configure in Jenkins)
        DOCKER_HUB_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKER_IMAGE = 'your-dockerhub-username/aceest-fitness'
        IMAGE_TAG = "${BUILD_NUMBER}"
        
        // SonarQube
        SONARQUBE_SERVER = 'SonarQube'
        SONAR_PROJECT_KEY = 'aceest-fitness'
        
        // Kubernetes
        KUBECONFIG = credentials('kubernetes-config')
    }
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
    }
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    echo "🔄 Checking out code from Git..."
                    checkout scm
                    
                    // Get Git commit info
                    env.GIT_COMMIT_SHORT = sh(
                        script: "git rev-parse --short HEAD",
                        returnStdout: true
                    ).trim()
                    
                    echo "📦 Building version: ${IMAGE_TAG} (${GIT_COMMIT_SHORT})"
                }
            }
        }
        
        stage('Setup Environment') {
            steps {
                script {
                    echo "🔧 Setting up Python virtual environment..."
                    sh '''
                        python -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                }
            }
        }
        
        stage('Lint & Code Quality') {
            steps {
                script {
                    echo "🔍 Running code quality checks..."
                    sh '''
                        . venv/bin/activate
                        pip install pylint flake8
                        
                        echo "Running Flake8..."
                        flake8 app.py --max-line-length=120 --ignore=E501,W503 || true
                        
                        echo "Running Pylint..."
                        pylint app.py --disable=C0111,C0103 --max-line-length=120 || true
                    '''
                }
            }
        }
        
        stage('Unit Tests') {
            steps {
                script {
                    echo "🧪 Running unit tests..."
                    sh '''
                        . venv/bin/activate
                        pytest tests/ -v --junitxml=test-results.xml --cov=app --cov-report=xml --cov-report=html
                    '''
                }
            }
            post {
                always {
                    junit 'test-results.xml'
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                script {
                    echo "📊 Running SonarQube analysis..."
                    withSonarQubeEnv("${SONARQUBE_SERVER}") {
                        sh '''
                            sonar-scanner \
                                -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                                -Dsonar.sources=. \
                                -Dsonar.exclusions=venv/**,tests/**,static/** \
                                -Dsonar.python.coverage.reportPaths=coverage.xml \
                                -Dsonar.python.xunit.reportPath=test-results.xml
                        '''
                    }
                }
            }
        }
        
        stage('Quality Gate') {
            steps {
                script {
                    echo "🚦 Waiting for SonarQube Quality Gate..."
                    timeout(time: 5, unit: 'MINUTES') {
                        waitForQualityGate abortPipeline: true
                    }
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo "🐳 Building Docker image..."
                    sh """
                        docker build \
                            --tag ${DOCKER_IMAGE}:${IMAGE_TAG} \
                            --tag ${DOCKER_IMAGE}:latest \
                            --build-arg BUILD_DATE=\$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
                            --build-arg VCS_REF=${GIT_COMMIT_SHORT} \
                            --build-arg VERSION=${IMAGE_TAG} \
                            .
                    """
                    
                    // Test the image
                    echo "✅ Testing Docker image..."
                    sh """
                        docker run --rm -d --name test-container -p 5001:5000 ${DOCKER_IMAGE}:${IMAGE_TAG}
                        sleep 10
                        curl -f http://localhost:5001/health || exit 1
                        docker stop test-container
                    """
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                script {
                    echo "🔒 Running security scan with Trivy..."
                    sh """
                        docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
                            aquasec/trivy image --severity HIGH,CRITICAL \
                            ${DOCKER_IMAGE}:${IMAGE_TAG} || true
                    """
                }
            }
        }
        
        stage('Push to Docker Hub') {
            when {
                branch 'main'
            }
            steps {
                script {
                    echo "📤 Pushing Docker image to Docker Hub..."
                    sh """
                        echo \${DOCKER_HUB_CREDENTIALS_PSW} | docker login -u \${DOCKER_HUB_CREDENTIALS_USR} --password-stdin
                        docker push ${DOCKER_IMAGE}:${IMAGE_TAG}
                        docker push ${DOCKER_IMAGE}:latest
                        docker logout
                    """
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            when {
                branch 'main'
            }
            steps {
                script {
                    echo "☸️ Deploying to Kubernetes..."
                    sh """
                        export KUBECONFIG=${KUBECONFIG}
                        
                        # Update deployment with new image
                        kubectl set image deployment/aceest-fitness-app \
                            aceest-fitness=${DOCKER_IMAGE}:${IMAGE_TAG} \
                            -n production
                        
                        # Wait for rollout
                        kubectl rollout status deployment/aceest-fitness-app -n production --timeout=5m
                        
                        # Verify deployment
                        kubectl get pods -n production -l app=aceest-fitness
                    """
                }
            }
        }
        
        stage('Smoke Tests') {
            when {
                branch 'main'
            }
            steps {
                script {
                    echo "🔥 Running smoke tests..."
                    sh '''
                        # Wait for service to be ready
                        sleep 30
                        
                        # Test health endpoint
                        curl -f http://your-kubernetes-service-url/health || exit 1
                        
                        echo "✅ Smoke tests passed!"
                    '''
                }
            }
        }
    }
    
    post {
        always {
            script {
                echo "🧹 Cleaning up..."
                sh '''
                    docker system prune -f
                    rm -rf venv
                '''
            }
            cleanWs()
        }
        
        success {
            script {
                echo "✅ Pipeline completed successfully!"
                // Send notifications (Slack, email, etc.)
                // slackSend color: 'good', message: "Build ${BUILD_NUMBER} succeeded"
            }
        }
        
        failure {
            script {
                echo "❌ Pipeline failed!"
                // Send failure notifications
                // slackSend color: 'danger', message: "Build ${BUILD_NUMBER} failed"
            }
        }
    }
}
