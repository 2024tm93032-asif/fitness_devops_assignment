#!/bin/bash

# Blue-Green Deployment Switch Script

NAMESPACE="aceest-fitness"
SERVICE_NAME="aceest-fitness-service"
CURRENT_VERSION=$(kubectl get service ${SERVICE_NAME} -n ${NAMESPACE} -o jsonpath='{.spec.selector.version}')

echo "Current active version: ${CURRENT_VERSION}"

if [ "$CURRENT_VERSION" == "blue" ]; then
    NEW_VERSION="green"
else
    NEW_VERSION="blue"
fi

echo "Switching to version: ${NEW_VERSION}"

# Update service selector to point to new version
kubectl patch service ${SERVICE_NAME} -n ${NAMESPACE} -p "{\"spec\":{\"selector\":{\"version\":\"${NEW_VERSION}\"}}}"

if [ $? -eq 0 ]; then
    echo "✅ Successfully switched to ${NEW_VERSION} version"
    echo "Testing new version..."
    
    sleep 10
    
    # Test the new version
    kubectl run test-pod --rm -i --restart=Never --image=curlimages/curl -- curl -f http://${SERVICE_NAME}.${NAMESPACE}/health
    
    if [ $? -eq 0 ]; then
        echo "✅ New version is healthy"
        echo "To rollback, run: kubectl patch service ${SERVICE_NAME} -n ${NAMESPACE} -p '{\"spec\":{\"selector\":{\"version\":\"${CURRENT_VERSION}\"}}}'"
    else
        echo "❌ New version health check failed! Rolling back..."
        kubectl patch service ${SERVICE_NAME} -n ${NAMESPACE} -p "{\"spec\":{\"selector\":{\"version\":\"${CURRENT_VERSION}\"}}}"
        exit 1
    fi
else
    echo "❌ Failed to switch versions"
    exit 1
fi
