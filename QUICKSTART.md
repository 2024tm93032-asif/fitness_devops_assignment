# 🚀 Quick Start Guide

Get ACEest Fitness up and running in 5 minutes!

## Prerequisites

- Python 3.11+
- Git
- Docker (optional)
- kubectl and Minikube (optional, for Kubernetes)

## Option 1: Run Locally (Fastest)

```bash
# 1. Clone repository
git clone <your-repo-url>
cd aceest-fitness

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application
python app.py

# 5. Open browser
# Visit: http://localhost:5000
```

## Option 2: Run with Docker

```bash
# 1. Clone repository
git clone <your-repo-url>
cd aceest-fitness

# 2. Build and run with Docker Compose
docker-compose up -d

# 3. Open browser
# Visit: http://localhost
```

## Option 3: Deploy to Kubernetes (Minikube)

```bash
# 1. Start Minikube
minikube start

# 2. Clone repository
git clone <your-repo-url>
cd aceest-fitness

# 3. Update Docker image in k8s/deployment.yaml
# Change: your-dockerhub-username/aceest-fitness:latest
# To your actual image

# 4. Deploy application
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# 5. Access application
minikube service aceest-fitness-service -n aceest-fitness
```

## Testing the Application

### Run Tests
```bash
# Activate virtual environment first
source venv/bin/activate

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=app --cov-report=html
```

## First Steps in the Application

1. **Register**: Create a new account
   - Username, password, name
   - Age, gender, height, weight
   - BMI and BMR are calculated automatically

2. **Login**: Sign in with your credentials

3. **Log Workouts**: 
   - Select category (Warm-up, Workout, Cool-down, etc.)
   - Enter exercise name
   - Enter duration
   - Calories burned are calculated automatically

4. **View Progress**: Check your workout statistics and charts

5. **Diet Guide**: See personalized nutrition recommendations

## Setup CI/CD Pipeline

### 1. Setup Git Repository

```bash
# Initialize Git (if not already done)
git init
git add .
git commit -m "chore: initial commit"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/yourusername/aceest-fitness.git
git push -u origin main
```

### 2. Setup Jenkins

1. Install Jenkins
2. Install required plugins:
   - Docker Pipeline
   - Kubernetes CLI
   - SonarQube Scanner
   - Git Plugin

3. Configure credentials:
   - Docker Hub credentials (ID: `dockerhub-credentials`)
   - Kubernetes config (ID: `kubernetes-config`)

4. Create Pipeline:
   - New Item → Pipeline
   - Configure Git repository
   - Set Script Path to `Jenkinsfile`
   - Enable GitHub webhook trigger

5. Run build!

### 3. Setup SonarQube (Optional)

```bash
# Run SonarQube with Docker
docker run -d --name sonarqube -p 9000:9000 sonarqube:latest

# Access: http://localhost:9000
# Default credentials: admin/admin

# Configure in Jenkins:
# Manage Jenkins → Configure System → SonarQube servers
# Add server: http://localhost:9000
```

## Deployment Strategies Quick Reference

### Rolling Update (Default)
```bash
kubectl set image deployment/aceest-fitness-app \
  aceest-fitness=yourusername/aceest-fitness:v1.1.0 \
  -n aceest-fitness
```

### Blue-Green Deployment
```bash
kubectl apply -f k8s/blue-green/
bash k8s/blue-green/switch.sh
```

### Canary Deployment
```bash
kubectl apply -f k8s/canary/deployment.yaml
bash k8s/canary/gradual-rollout.sh
```

## Common Issues and Solutions

### Issue: Module not found
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

### Issue: Port already in use
```bash
# Solution: Change port
export PORT=5001
python app.py
```

### Issue: Docker permission denied
```bash
# Solution: Add user to docker group
sudo usermod -aG docker $USER
# Logout and login again
```

### Issue: Kubernetes pods not starting
```bash
# Check pod status
kubectl get pods -n aceest-fitness

# Check logs
kubectl logs <pod-name> -n aceest-fitness

# Describe pod for details
kubectl describe pod <pod-name> -n aceest-fitness
```

## Environment Variables

Create a `.env` file:

```env
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-change-in-production
PORT=5000
```

## Next Steps

1. ✅ Application running locally
2. 📚 Read full [README.md](README.md)
3. 🐳 Try Docker deployment
4. ☸️ Deploy to Kubernetes
5. 🔄 Setup Jenkins pipeline
6. 📊 Configure monitoring

## Need Help?

- 📖 Check [README.md](README.md) for detailed documentation
- 🐳 See [DOCKER.md](DOCKER.md) for Docker guide
- ☸️ See [KUBERNETES.md](KUBERNETES.md) for K8s guide
- 🔧 See [JENKINS_SETUP.md](JENKINS_SETUP.md) for CI/CD setup
- 📝 Check [GIT_WORKFLOW.md](GIT_WORKFLOW.md) for Git practices

## Project Structure Overview

```
aceest-fitness/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container definition
├── docker-compose.yml    # Docker Compose config
├── Jenkinsfile          # CI/CD pipeline
├── templates/           # HTML templates
├── static/             # CSS, JS, images
├── tests/              # Test suite
└── k8s/                # Kubernetes manifests
```

## Health Check

Verify the application is running:

```bash
# Local
curl http://localhost:5000/health

# Docker
curl http://localhost/health

# Kubernetes
kubectl get pods -n aceest-fitness
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-11-10T12:00:00"
}
```

## Congratulations! 🎉

You've successfully set up ACEest Fitness! Now you can:
- Log workouts and track fitness
- View progress with charts
- Get diet recommendations
- Deploy with modern DevOps practices

Happy tracking! 💪
