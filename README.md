# ACEest Fitness & Gym Management System
## Complete DevOps Pipeline Implementation

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11-green)
![Flask](https://img.shields.io/badge/flask-3.0.0-lightgrey)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![Kubernetes](https://img.shields.io/badge/kubernetes-ready-blue)

A comprehensive fitness tracking and gym management web application with a complete CI/CD DevOps pipeline, demonstrating modern software delivery practices.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Development Setup](#development-setup)
- [Testing](#testing)
- [Docker Deployment](#docker-deployment)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Advanced Deployment Strategies](#advanced-deployment-strategies)
- [CI/CD Pipeline](#cicd-pipeline)
- [Monitoring and Logging](#monitoring-and-logging)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

ACEest Fitness is a modern web-based fitness and gym management system built to demonstrate enterprise-level DevOps practices. This project showcases the complete software development lifecycle from code to production deployment with automated testing, continuous integration, and multiple deployment strategies.

### Assignment Objectives ✓

- ✅ Flask web application development
- ✅ Git version control with structured workflow
- ✅ Comprehensive unit testing with Pytest
- ✅ Jenkins CI/CD pipeline
- ✅ Docker containerization
- ✅ Kubernetes orchestration
- ✅ Advanced deployment strategies (Blue-Green, Canary, A/B, Shadow, Rolling)
- ✅ SonarQube code quality analysis
- ✅ Automated rollback mechanisms

---

## ✨ Features

### Application Features
- 👤 User registration and authentication
- 🏋️ Workout logging and tracking
- 📊 Progress visualization with charts
- 🔥 Calorie calculation based on MET values
- 📈 BMI and BMR calculations
- 🥗 Personalized diet recommendations
- 📱 Responsive web design

### DevOps Features
- 🔄 Automated CI/CD pipeline
- 🐳 Multi-stage Docker builds
- ☸️ Kubernetes orchestration
- 🔵🟢 Blue-Green deployments
- 🐤 Canary releases
- 🎯 A/B testing support
- 👥 Shadow deployments
- 🔄 Rolling updates
- 📊 Code quality gates with SonarQube
- 🧪 Automated testing
- 🔒 Container security scanning
- 📦 Docker Hub integration

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Users/Clients                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Kubernetes Ingress                         │
│                    (Load Balancer)                           │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Pod 1     │  │   Pod 2     │  │   Pod 3     │
│  Flask App  │  │  Flask App  │  │  Flask App  │
└─────────────┘  └─────────────┘  └─────────────┘

┌─────────────────────────────────────────────────────────────┐
│                     CI/CD Pipeline                           │
│                                                              │
│  GitHub → Jenkins → Tests → SonarQube → Docker → K8s        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

### Backend
- **Python 3.11**: Core programming language
- **Flask 3.0**: Web framework
- **Gunicorn**: WSGI HTTP server

### Frontend
- **HTML5/CSS3**: Structure and styling
- **JavaScript**: Client-side interactivity
- **Chart.js**: Data visualization

### Testing
- **Pytest**: Unit testing framework
- **pytest-flask**: Flask testing utilities
- **pytest-cov**: Code coverage

### DevOps Tools
- **Git/GitHub**: Version control
- **Docker**: Containerization
- **Docker Hub**: Container registry
- **Kubernetes**: Container orchestration
- **Jenkins**: CI/CD automation
- **SonarQube**: Code quality analysis
- **Trivy**: Security scanning

### Deployment
- **Minikube**: Local Kubernetes
- **AWS/Azure/GCP**: Cloud platforms (optional)
- **Nginx**: Reverse proxy

---

## 📁 Project Structure

```
aceest-fitness/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── pytest.ini                  # Pytest configuration
├── .gitignore                  # Git ignore rules
├── .env.example                # Environment variables template
│
├── templates/                  # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── workouts.html
│   ├── progress.html
│   └── diet.html
│
├── static/                     # Static assets
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
│
├── tests/                      # Test suite
│   ├── __init__.py
│   └── test_app.py
│
├── k8s/                        # Kubernetes manifests
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── hpa.yaml
│   │
│   ├── blue-green/             # Blue-Green deployment
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── switch.sh
│   │
│   ├── canary/                 # Canary deployment
│   │   ├── deployment.yaml
│   │   └── gradual-rollout.sh
│   │
│   └── ab-testing/             # A/B testing & Shadow
│       ├── istio-ab.yaml
│       └── shadow-deployment.yaml
│
├── Dockerfile                  # Multi-stage Docker build
├── docker-compose.yml          # Docker Compose configuration
├── docker-build.sh             # Docker build script
├── nginx.conf                  # Nginx configuration
│
├── Jenkinsfile                 # Jenkins pipeline
├── sonar-project.properties    # SonarQube configuration
│
└── docs/                       # Documentation
    ├── GIT_WORKFLOW.md
    ├── DOCKER.md
    ├── JENKINS_SETUP.md
    └── KUBERNETES.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Git
- Kubernetes cluster (Minikube for local)
- Jenkins (optional, for CI/CD)

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/aceest-fitness.git
cd aceest-fitness
```

### 2. Run Locally
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

Access at: http://localhost:5000

### 3. Run with Docker
```bash
docker-compose up -d
```

Access at: http://localhost

### 4. Run Tests
```bash
pytest tests/ -v --cov=app
```

---

## 💻 Development Setup

### 1. Setup Development Environment
```bash
# Clone repository
git clone <repo-url>
cd aceest-fitness

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your configuration
```

### 2. Configure Git
```bash
# Initialize Git (if not already done)
git init

# Configure user
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Create develop branch
git checkout -b develop
```

### 3. Run Development Server
```bash
export FLASK_ENV=development
export FLASK_APP=app.py
flask run --debug
```

---

## 🧪 Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run with Coverage
```bash
pytest tests/ -v --cov=app --cov-report=html
```

### Run Specific Test File
```bash
pytest tests/test_app.py -v
```

### Generate Coverage Report
```bash
pytest tests/ --cov=app --cov-report=html
# Open htmlcov/index.html in browser
```

### Test Categories
- **Unit Tests**: Test individual functions
- **Integration Tests**: Test API endpoints
- **Authentication Tests**: Test login/registration
- **Workout Tests**: Test workout logging
- **Edge Cases**: Test error handling

---

## 🐳 Docker Deployment

### Build Image
```bash
docker build -t aceest-fitness:latest .
```

### Run Container
```bash
docker run -d -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret-key \
  --name aceest-app \
  aceest-fitness:latest
```

### Docker Compose
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Push to Docker Hub
```bash
# Login
docker login

# Tag image
docker tag aceest-fitness:latest yourusername/aceest-fitness:v1.0.0

# Push
docker push yourusername/aceest-fitness:v1.0.0
docker push yourusername/aceest-fitness:latest
```

---

## ☸️ Kubernetes Deployment

### Setup Minikube (Local)
```bash
# Start Minikube
minikube start --memory=4096 --cpus=2

# Enable addons
minikube addons enable ingress
minikube addons enable metrics-server
```

### Deploy Application
```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Deploy config and secrets
kubectl apply -f k8s/configmap.yaml

# Deploy application
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

# Enable autoscaling
kubectl apply -f k8s/hpa.yaml
```

### Verify Deployment
```bash
# Check pods
kubectl get pods -n aceest-fitness

# Check services
kubectl get svc -n aceest-fitness

# Check deployments
kubectl get deployments -n aceest-fitness

# View logs
kubectl logs -f deployment/aceest-fitness-app -n aceest-fitness
```

### Access Application
```bash
# Get service URL (Minikube)
minikube service aceest-fitness-service -n aceest-fitness

# Or port-forward
kubectl port-forward svc/aceest-fitness-service 8080:80 -n aceest-fitness
```

---

## 🎯 Advanced Deployment Strategies

### 1. Blue-Green Deployment
Zero-downtime deployment with instant rollback.

```bash
# Deploy both versions
kubectl apply -f k8s/blue-green/deployment.yaml

# Switch traffic to green
bash k8s/blue-green/switch.sh

# Rollback if needed (switch back to blue)
kubectl patch service aceest-fitness-service -n aceest-fitness \
  -p '{"spec":{"selector":{"version":"blue"}}}'
```

**Benefits:**
- Zero downtime
- Instant rollback
- Easy testing of new version

### 2. Canary Deployment
Gradual rollout to minimize risk.

```bash
# Deploy stable and canary
kubectl apply -f k8s/canary/deployment.yaml

# Gradual rollout (10% → 25% → 50% → 75% → 100%)
bash k8s/canary/gradual-rollout.sh
```

**Traffic Distribution:**
- Stage 1: 10% canary, 90% stable
- Stage 2: 25% canary, 75% stable
- Stage 3: 50% canary, 50% stable
- Stage 4: 75% canary, 25% stable
- Stage 5: 100% canary

### 3. A/B Testing
Test different versions with specific user groups.

```bash
# Requires Istio service mesh
kubectl apply -f k8s/ab-testing/istio-ab.yaml
```

**Routing Rules:**
- Users with header `user-group: beta` → Version B
- All other users → 50/50 split between A and B

### 4. Shadow Deployment
Test new version with production traffic without affecting users.

```bash
kubectl apply -f k8s/ab-testing/shadow-deployment.yaml
```

**How it works:**
- All traffic goes to production version
- Traffic is mirrored to shadow version
- Shadow responses are discarded
- Monitor shadow version for errors

### 5. Rolling Update
Default Kubernetes strategy.

```bash
# Update image
kubectl set image deployment/aceest-fitness-app \
  aceest-fitness=yourusername/aceest-fitness:v1.1.0 \
  -n aceest-fitness

# Monitor rollout
kubectl rollout status deployment/aceest-fitness-app -n aceest-fitness

# Rollback if needed
kubectl rollout undo deployment/aceest-fitness-app -n aceest-fitness
```

---

## 🔄 CI/CD Pipeline

### Jenkins Pipeline Stages

1. **Checkout**: Clone repository from Git
2. **Setup Environment**: Install Python dependencies
3. **Lint & Code Quality**: Run flake8 and pylint
4. **Unit Tests**: Execute pytest with coverage
5. **SonarQube Analysis**: Analyze code quality
6. **Quality Gate**: Wait for SonarQube results
7. **Build Docker Image**: Create container image
8. **Security Scan**: Scan with Trivy
9. **Push to Docker Hub**: Upload image to registry
10. **Deploy to Kubernetes**: Update K8s deployment
11. **Smoke Tests**: Verify deployment

### Trigger Build
- **Automatic**: Git push triggers webhook
- **Manual**: Click "Build Now" in Jenkins
- **Scheduled**: Cron-based builds

### View Results
- Jenkins Dashboard: Build status
- Coverage Report: Code coverage metrics
- SonarQube: Code quality analysis
- Test Results: JUnit test reports

---

## 📊 Monitoring and Logging

### Health Check
```bash
curl http://your-app-url/health
```

### Kubernetes Monitoring
```bash
# Pod metrics
kubectl top pods -n aceest-fitness

# Node metrics
kubectl top nodes

# Horizontal Pod Autoscaler status
kubectl get hpa -n aceest-fitness
```

### View Logs
```bash
# Application logs
kubectl logs -f deployment/aceest-fitness-app -n aceest-fitness

# Previous logs (for crashed pods)
kubectl logs deployment/aceest-fitness-app -n aceest-fitness --previous

# All pods logs
kubectl logs -l app=aceest-fitness -n aceest-fitness
```

---

## 🤝 Contributing

### Git Workflow
See [GIT_WORKFLOW.md](GIT_WORKFLOW.md) for detailed workflow.

1. Create feature branch
2. Make changes
3. Write tests
4. Commit with conventional messages
5. Push and create Pull Request

### Commit Message Format
```
<type>(<scope>): <subject>

Examples:
feat(auth): add password reset functionality
fix(workout): correct calorie calculation
docs(readme): update installation instructions
test(api): add workout endpoint tests
```

---

## 📚 Additional Documentation

- [Git Workflow](GIT_WORKFLOW.md) - Branching strategy and version control
- [Docker Guide](DOCKER.md) - Container build and deployment
- [Jenkins Setup](JENKINS_SETUP.md) - CI/CD pipeline configuration
- [Kubernetes Guide](KUBERNETES.md) - Orchestration and deployment

