# Docker Commands Reference

## Build and Run Locally

### Build Docker Image
```bash
docker build -t aceest-fitness:latest .
```

### Run Container
```bash
docker run -d -p 5000:5000 --name aceest-app aceest-fitness:latest
```

### Run with Docker Compose
```bash
docker-compose up -d
```

### Stop and Remove
```bash
docker-compose down
```

### View Logs
```bash
docker logs aceest-fitness-app
docker-compose logs -f app
```

## Docker Hub

### Login to Docker Hub
```bash
docker login
```

### Tag Image
```bash
docker tag aceest-fitness:latest your-username/aceest-fitness:v1.0.0
```

### Push to Docker Hub
```bash
docker push your-username/aceest-fitness:v1.0.0
docker push your-username/aceest-fitness:latest
```

### Pull from Docker Hub
```bash
docker pull your-username/aceest-fitness:latest
```

## Useful Commands

### List Images
```bash
docker images
```

### List Containers
```bash
docker ps -a
```

### Remove Image
```bash
docker rmi aceest-fitness:latest
```

### Remove Container
```bash
docker rm aceest-fitness-app
```

### Execute Command in Container
```bash
docker exec -it aceest-fitness-app /bin/bash
```

### Inspect Container
```bash
docker inspect aceest-fitness-app
```

### View Resource Usage
```bash
docker stats aceest-fitness-app
```

## Multi-stage Build Benefits
- Smaller final image size
- Improved security (no build tools in runtime)
- Faster deployment
- Clean separation of build and runtime dependencies

## Health Checks
The Dockerfile includes health checks:
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')"
```

Check health status:
```bash
docker inspect --format='{{.State.Health.Status}}' aceest-fitness-app
```
