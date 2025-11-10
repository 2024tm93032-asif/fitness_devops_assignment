# Kubernetes Deployment Guide

## Table of Contents
- [Prerequisites](#prerequisites)
- [Setup Kubernetes Cluster](#setup-kubernetes-cluster)
- [Deploy Application](#deploy-application)
- [Advanced Deployments](#advanced-deployments)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- Kubernetes cluster (Minikube, EKS, GKE, or AKS)
- kubectl CLI tool
- Docker Hub account with pushed images
- Basic understanding of Kubernetes concepts

## Setup Kubernetes Cluster

### Option 1: Local with Minikube

```bash
# Install Minikube
# macOS
brew install minikube

# Windows (using Chocolatey)
choco install minikube

# Linux
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Start Minikube
minikube start --memory=4096 --cpus=2 --driver=docker

# Enable addons
minikube addons enable ingress
minikube addons enable metrics-server
minikube addons enable dashboard

# Verify
kubectl cluster-info
kubectl get nodes
```

### Option 2: AWS EKS

```bash
# Install eksctl
brew install eksctl  # macOS
choco install eksctl # Windows

# Create cluster
eksctl create cluster \
  --name aceest-fitness \
  --region us-east-1 \
  --nodes 3 \
  --node-type t3.medium

# Configure kubectl
aws eks update-kubeconfig --name aceest-fitness --region us-east-1
```

### Option 3: Google GKE

```bash
# Create cluster
gcloud container clusters create aceest-fitness \
  --num-nodes=3 \
  --machine-type=e2-medium \
  --region=us-central1

# Get credentials
gcloud container clusters get-credentials aceest-fitness --region=us-central1
```

## Deploy Application

### Step 1: Create Namespace

```bash
kubectl apply -f k8s/namespace.yaml

# Verify
kubectl get namespaces
```

### Step 2: Deploy ConfigMap and Secrets

```bash
# Update secrets first
kubectl create secret generic aceest-fitness-secret \
  --from-literal=SECRET_KEY='your-production-secret-key' \
  -n aceest-fitness

# Or use the YAML file (update values first)
kubectl apply -f k8s/configmap.yaml
```

### Step 3: Deploy Application

```bash
# Update image in deployment.yaml first
# Replace: your-dockerhub-username/aceest-fitness:latest
# With your actual image

kubectl apply -f k8s/deployment.yaml

# Wait for deployment
kubectl rollout status deployment/aceest-fitness-app -n aceest-fitness

# Check pods
kubectl get pods -n aceest-fitness
```

### Step 4: Create Service

```bash
kubectl apply -f k8s/service.yaml

# Get service details
kubectl get svc -n aceest-fitness

# For Minikube, get URL
minikube service aceest-fitness-service -n aceest-fitness --url
```

### Step 5: Setup Ingress

```bash
# Update host in ingress.yaml
kubectl apply -f k8s/ingress.yaml

# Get ingress IP
kubectl get ingress -n aceest-fitness

# For Minikube
minikube ip
# Add to /etc/hosts: <minikube-ip> aceest-fitness.local
```

### Step 6: Enable Autoscaling

```bash
kubectl apply -f k8s/hpa.yaml

# Check HPA status
kubectl get hpa -n aceest-fitness

# Watch autoscaling
kubectl get hpa -n aceest-fitness -w
```

## Access Application

### Minikube

```bash
# Option 1: Service URL
minikube service aceest-fitness-service -n aceest-fitness

# Option 2: Port Forward
kubectl port-forward svc/aceest-fitness-service 8080:80 -n aceest-fitness
# Access: http://localhost:8080

# Option 3: Ingress (if configured)
# Add to /etc/hosts: $(minikube ip) aceest-fitness.local
# Access: http://aceest-fitness.local
```

### Cloud Providers

```bash
# Get LoadBalancer external IP
kubectl get svc aceest-fitness-service -n aceest-fitness

# Access via external IP
curl http://<EXTERNAL-IP>/health
```

## Advanced Deployments

### Rolling Update

```bash
# Update image version
kubectl set image deployment/aceest-fitness-app \
  aceest-fitness=yourusername/aceest-fitness:v1.1.0 \
  -n aceest-fitness

# Monitor rollout
kubectl rollout status deployment/aceest-fitness-app -n aceest-fitness

# Check history
kubectl rollout history deployment/aceest-fitness-app -n aceest-fitness

# Rollback if needed
kubectl rollout undo deployment/aceest-fitness-app -n aceest-fitness
```

### Blue-Green Deployment

```bash
# Deploy both versions
kubectl apply -f k8s/blue-green/deployment.yaml
kubectl apply -f k8s/blue-green/service.yaml

# Verify both are running
kubectl get deployments -n aceest-fitness

# Switch to green (automated script)
bash k8s/blue-green/switch.sh

# Manual switch
kubectl patch service aceest-fitness-service -n aceest-fitness \
  -p '{"spec":{"selector":{"version":"green"}}}'

# Rollback to blue
kubectl patch service aceest-fitness-service -n aceest-fitness \
  -p '{"spec":{"selector":{"version":"blue"}}}'
```

### Canary Deployment

```bash
# Deploy stable and canary
kubectl apply -f k8s/canary/deployment.yaml

# Check replica distribution
kubectl get deployments -n aceest-fitness

# Gradual rollout
bash k8s/canary/gradual-rollout.sh

# Manual scaling
kubectl scale deployment aceest-fitness-stable --replicas=9 -n aceest-fitness
kubectl scale deployment aceest-fitness-canary --replicas=1 -n aceest-fitness

# Promote canary to stable
CANARY_IMAGE=$(kubectl get deployment aceest-fitness-canary -n aceest-fitness -o jsonpath='{.spec.template.spec.containers[0].image}')
kubectl set image deployment/aceest-fitness-stable aceest-fitness=$CANARY_IMAGE -n aceest-fitness
kubectl scale deployment aceest-fitness-canary --replicas=0 -n aceest-fitness
```

### A/B Testing (Requires Istio)

```bash
# Install Istio
istioctl install --set profile=demo -y

# Label namespace for Istio injection
kubectl label namespace aceest-fitness istio-injection=enabled

# Deploy A/B testing configuration
kubectl apply -f k8s/ab-testing/istio-ab.yaml

# Test routing
# Beta users (with header)
curl -H "user-group: beta" http://aceest-fitness-service/

# Regular users (50/50 split)
curl http://aceest-fitness-service/
```

### Shadow Deployment

```bash
# Deploy shadow configuration
kubectl apply -f k8s/ab-testing/shadow-deployment.yaml

# Monitor shadow logs
kubectl logs -f deployment/aceest-fitness-shadow -n aceest-fitness

# Check error rates
kubectl logs deployment/aceest-fitness-shadow -n aceest-fitness | grep ERROR
```

## Monitoring

### Pod Status

```bash
# List all pods
kubectl get pods -n aceest-fitness

# Detailed pod info
kubectl describe pod <pod-name> -n aceest-fitness

# Pod logs
kubectl logs -f <pod-name> -n aceest-fitness

# Previous logs (crashed pods)
kubectl logs <pod-name> -n aceest-fitness --previous

# Logs from all pods
kubectl logs -l app=aceest-fitness -n aceest-fitness
```

### Resource Usage

```bash
# Pod metrics
kubectl top pods -n aceest-fitness

# Node metrics
kubectl top nodes

# HPA status
kubectl get hpa -n aceest-fitness -w
```

### Events

```bash
# Namespace events
kubectl get events -n aceest-fitness --sort-by='.lastTimestamp'

# Deployment events
kubectl describe deployment aceest-fitness-app -n aceest-fitness
```

### Dashboard

```bash
# Minikube dashboard
minikube dashboard

# Or start proxy
kubectl proxy
# Access: http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/
```

## Scaling

### Manual Scaling

```bash
# Scale deployment
kubectl scale deployment aceest-fitness-app --replicas=5 -n aceest-fitness

# Verify
kubectl get deployments -n aceest-fitness
```

### Autoscaling

```bash
# HPA is already configured in k8s/hpa.yaml
# Check status
kubectl get hpa -n aceest-fitness

# Edit HPA
kubectl edit hpa aceest-fitness-hpa -n aceest-fitness

# Delete HPA
kubectl delete hpa aceest-fitness-hpa -n aceest-fitness
```

## Troubleshooting

### Pod Not Starting

```bash
# Check pod status
kubectl get pods -n aceest-fitness

# Describe pod for events
kubectl describe pod <pod-name> -n aceest-fitness

# Check logs
kubectl logs <pod-name> -n aceest-fitness

# Common issues:
# - Image pull errors: Check image name and credentials
# - Resource limits: Check node capacity
# - ConfigMap/Secret missing: Verify they exist
```

### Service Not Accessible

```bash
# Check service
kubectl get svc -n aceest-fitness

# Check endpoints
kubectl get endpoints -n aceest-fitness

# Test from within cluster
kubectl run test --rm -it --image=curlimages/curl -- sh
curl http://aceest-fitness-service.aceest-fitness/health
```

### Image Pull Errors

```bash
# Create Docker Hub secret
kubectl create secret docker-registry dockerhub-secret \
  --docker-server=docker.io \
  --docker-username=<your-username> \
  --docker-password=<your-password> \
  --docker-email=<your-email> \
  -n aceest-fitness

# Update deployment to use secret
# Add to spec.template.spec:
imagePullSecrets:
- name: dockerhub-secret
```

### High Memory/CPU Usage

```bash
# Check resource usage
kubectl top pods -n aceest-fitness

# Adjust resource limits in deployment.yaml
# Increase limits if pods are being killed
# Increase requests if pods aren't scheduling
```

## Cleanup

### Delete Application

```bash
# Delete all resources
kubectl delete -f k8s/deployment.yaml
kubectl delete -f k8s/service.yaml
kubectl delete -f k8s/ingress.yaml
kubectl delete -f k8s/hpa.yaml
kubectl delete -f k8s/configmap.yaml

# Or delete namespace (removes everything)
kubectl delete namespace aceest-fitness
```

### Delete Cluster

```bash
# Minikube
minikube delete

# EKS
eksctl delete cluster --name aceest-fitness --region us-east-1

# GKE
gcloud container clusters delete aceest-fitness --region=us-central1
```

## Best Practices

1. **Use Namespaces**: Isolate environments
2. **Resource Limits**: Always set requests and limits
3. **Health Checks**: Configure liveness and readiness probes
4. **Secrets Management**: Never commit secrets to Git
5. **Rolling Updates**: Use for zero-downtime deployments
6. **Monitoring**: Set up proper logging and monitoring
7. **Backup**: Regular backup of ConfigMaps and Secrets
8. **RBAC**: Implement proper access controls
9. **Network Policies**: Restrict pod-to-pod communication
10. **Labels**: Use consistent labeling strategy

## Useful Commands

```bash
# Get everything in namespace
kubectl get all -n aceest-fitness

# Describe all resources
kubectl describe all -n aceest-fitness

# Delete stuck pods
kubectl delete pod <pod-name> -n aceest-fitness --force --grace-period=0

# Port forward to pod
kubectl port-forward <pod-name> 8080:5000 -n aceest-fitness

# Execute command in pod
kubectl exec -it <pod-name> -n aceest-fitness -- /bin/bash

# Copy files to/from pod
kubectl cp <local-path> <pod-name>:<pod-path> -n aceest-fitness

# Apply all manifests in directory
kubectl apply -f k8s/ -n aceest-fitness

# Watch pods
kubectl get pods -n aceest-fitness -w
```
