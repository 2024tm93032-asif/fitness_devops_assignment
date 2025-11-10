# Docker Build and Push Script
# This script builds Docker images and pushes to Docker Hub

# Image name and version
IMAGE_NAME="aceest-fitness"
DOCKER_USERNAME="your-dockerhub-username"
VERSION=${1:-"latest"}

echo "Building Docker image..."
docker build -t ${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION} .

if [ $? -eq 0 ]; then
    echo "Build successful!"
    
    # Tag as latest
    docker tag ${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION} ${DOCKER_USERNAME}/${IMAGE_NAME}:latest
    
    echo "Pushing to Docker Hub..."
    docker push ${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION}
    docker push ${DOCKER_USERNAME}/${IMAGE_NAME}:latest
    
    echo "Docker image pushed successfully!"
    echo "Image: ${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION}"
else
    echo "Build failed!"
    exit 1
fi
