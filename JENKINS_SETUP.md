# Jenkins Setup Guide for ACEest Fitness Pipeline

## Prerequisites
- Jenkins 2.x or higher installed
- Docker installed on Jenkins server
- Kubernetes cluster configured
- SonarQube server setup

## Jenkins Plugins Required

Install the following plugins via Jenkins UI (Manage Jenkins > Manage Plugins):

1. **Essential Plugins**
   - Docker Pipeline
   - Kubernetes CLI Plugin
   - Git Plugin
   - Pipeline Plugin
   - SonarQube Scanner

2. **Optional but Recommended**
   - Blue Ocean (better UI)
   - Slack Notification
   - Email Extension
   - HTML Publisher
   - JUnit Plugin
   - Cobertura Plugin

## Configure Jenkins

### 1. Configure Docker Hub Credentials
```
Manage Jenkins > Credentials > System > Global credentials > Add Credentials
- Kind: Username with password
- ID: dockerhub-credentials
- Username: <your-dockerhub-username>
- Password: <your-dockerhub-password>
```

### 2. Configure Kubernetes
```
Manage Jenkins > Credentials > System > Global credentials > Add Credentials
- Kind: Secret file
- ID: kubernetes-config
- File: Upload your kubeconfig file
```

### 3. Configure SonarQube
```
Manage Jenkins > Configure System > SonarQube servers
- Name: SonarQube
- Server URL: http://your-sonarqube-server:9000
- Authentication token: Add from credentials
```

### 4. Install SonarQube Scanner
```
Manage Jenkins > Global Tool Configuration > SonarQube Scanner
- Name: SonarQube Scanner
- Install automatically
```

### 5. Configure GitHub Webhook
In your GitHub repository:
```
Settings > Webhooks > Add webhook
- Payload URL: http://your-jenkins-server/github-webhook/
- Content type: application/json
- Events: Just the push event
```

## Create Jenkins Pipeline Job

### Method 1: Pipeline from SCM
1. New Item > Pipeline
2. Configure:
   - Build Triggers: Check "GitHub hook trigger for GITScm polling"
   - Pipeline: Pipeline script from SCM
   - SCM: Git
   - Repository URL: Your GitHub repo URL
   - Credentials: Add GitHub credentials
   - Branch: */main
   - Script Path: Jenkinsfile

### Method 2: Multibranch Pipeline
1. New Item > Multibranch Pipeline
2. Configure:
   - Branch Sources: Git
   - Repository URL: Your GitHub repo
   - Credentials: GitHub credentials
   - Build Configuration: by Jenkinsfile

## Jenkins Pipeline Stages

The Jenkinsfile includes the following stages:

1. **Checkout**: Clone the repository
2. **Setup Environment**: Install Python dependencies
3. **Lint & Code Quality**: Run flake8 and pylint
4. **Unit Tests**: Execute pytest with coverage
5. **SonarQube Analysis**: Code quality analysis
6. **Quality Gate**: Wait for SonarQube results
7. **Build Docker Image**: Create Docker image
8. **Security Scan**: Scan image with Trivy
9. **Push to Docker Hub**: Push image to registry
10. **Deploy to Kubernetes**: Update K8s deployment
11. **Smoke Tests**: Verify deployment

## Automated Build Triggers

### Poll SCM (Alternative to Webhooks)
```groovy
pipeline {
    triggers {
        pollSCM('H/5 * * * *')  // Poll every 5 minutes
    }
}
```

### Cron-based Builds
```groovy
pipeline {
    triggers {
        cron('H 2 * * *')  // Build daily at 2 AM
    }
}
```

### Parameterized Builds
```groovy
pipeline {
    parameters {
        choice(name: 'ENVIRONMENT', choices: ['dev', 'staging', 'production'])
        booleanParam(name: 'RUN_TESTS', defaultValue: true)
    }
}
```

## Build Artifacts

Jenkins stores the following artifacts:
- Test results (JUnit XML)
- Coverage reports (HTML)
- SonarQube analysis results
- Docker image tags

Access artifacts: Build > Build Artifacts

## Notifications

### Email Notifications
```groovy
post {
    failure {
        emailext (
            subject: "Build Failed: ${JOB_NAME} - ${BUILD_NUMBER}",
            body: "Check console output at ${BUILD_URL}",
            to: "team@example.com"
        )
    }
}
```

### Slack Notifications
```groovy
post {
    success {
        slackSend (
            color: 'good',
            message: "Build Successful: ${JOB_NAME} - ${BUILD_NUMBER}"
        )
    }
}
```

## Troubleshooting

### Docker Permission Issues
Add Jenkins user to docker group:
```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### Kubernetes Connection Issues
Verify kubeconfig:
```bash
kubectl --kubeconfig=/path/to/kubeconfig get nodes
```

### SonarQube Connection
Test from Jenkins server:
```bash
curl http://your-sonarqube-server:9000/api/system/status
```

## Best Practices

1. **Use Shared Libraries**: Create reusable pipeline functions
2. **Parallel Stages**: Run independent stages in parallel
3. **Timeout**: Set reasonable timeouts for stages
4. **Resource Cleanup**: Always clean up in post section
5. **Secret Management**: Use Jenkins credentials, never hardcode
6. **Build History**: Configure build retention policy
7. **Notifications**: Set up proper alerting channels

## Monitoring

Monitor Jenkins:
- Dashboard: http://your-jenkins-server/
- Blue Ocean: http://your-jenkins-server/blue/
- System Logs: Manage Jenkins > System Log

## Security

1. Enable authentication and authorization
2. Use HTTPS for Jenkins
3. Keep Jenkins and plugins updated
4. Use credentials binding for secrets
5. Implement role-based access control
6. Regular backup of Jenkins configuration
