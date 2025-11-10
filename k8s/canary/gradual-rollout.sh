#!/bin/bash

# Canary Deployment Gradual Rollout Script

NAMESPACE="aceest-fitness"
STABLE_DEPLOYMENT="aceest-fitness-stable"
CANARY_DEPLOYMENT="aceest-fitness-canary"

# Traffic distribution stages
STAGES=(10 25 50 75 100)

echo "Starting canary deployment..."

for PERCENTAGE in "${STAGES[@]}"; do
    CANARY_REPLICAS=$(( ($PERCENTAGE * 10) / 100 ))
    STABLE_REPLICAS=$(( 10 - $CANARY_REPLICAS ))
    
    echo "-----------------------------------"
    echo "Stage: ${PERCENTAGE}% traffic to canary"
    echo "Stable replicas: ${STABLE_REPLICAS}"
    echo "Canary replicas: ${CANARY_REPLICAS}"
    
    # Scale deployments
    kubectl scale deployment ${STABLE_DEPLOYMENT} -n ${NAMESPACE} --replicas=${STABLE_REPLICAS}
    kubectl scale deployment ${CANARY_DEPLOYMENT} -n ${NAMESPACE} --replicas=${CANARY_REPLICAS}
    
    # Wait for rollout
    kubectl rollout status deployment ${STABLE_DEPLOYMENT} -n ${NAMESPACE} --timeout=2m
    kubectl rollout status deployment ${CANARY_DEPLOYMENT} -n ${NAMESPACE} --timeout=2m
    
    # Monitor canary for issues
    echo "Monitoring canary for 60 seconds..."
    sleep 60
    
    # Check error rate (simplified)
    CANARY_PODS=$(kubectl get pods -n ${NAMESPACE} -l track=canary -o jsonpath='{.items[*].metadata.name}')
    ERROR_COUNT=0
    
    for POD in $CANARY_PODS; do
        RESTARTS=$(kubectl get pod $POD -n ${NAMESPACE} -o jsonpath='{.status.containerStatuses[0].restartCount}')
        ERROR_COUNT=$((ERROR_COUNT + RESTARTS))
    done
    
    if [ $ERROR_COUNT -gt 5 ]; then
        echo "❌ High error rate detected! Rolling back..."
        kubectl scale deployment ${STABLE_DEPLOYMENT} -n ${NAMESPACE} --replicas=10
        kubectl scale deployment ${CANARY_DEPLOYMENT} -n ${NAMESPACE} --replicas=0
        exit 1
    fi
    
    echo "✅ Stage ${PERCENTAGE}% successful"
    
    if [ $PERCENTAGE -ne 100 ]; then
        read -p "Continue to next stage? (y/n): " CONTINUE
        if [ "$CONTINUE" != "y" ]; then
            echo "Deployment paused at ${PERCENTAGE}%"
            exit 0
        fi
    fi
done

echo "✅ Canary deployment completed successfully!"
echo "Promoting canary to stable..."

# Update stable deployment to use canary image
CANARY_IMAGE=$(kubectl get deployment ${CANARY_DEPLOYMENT} -n ${NAMESPACE} -o jsonpath='{.spec.template.spec.containers[0].image}')
kubectl set image deployment/${STABLE_DEPLOYMENT} -n ${NAMESPACE} aceest-fitness=${CANARY_IMAGE}

# Scale back to normal
kubectl scale deployment ${STABLE_DEPLOYMENT} -n ${NAMESPACE} --replicas=10
kubectl scale deployment ${CANARY_DEPLOYMENT} -n ${NAMESPACE} --replicas=0

echo "✅ Deployment complete!"
