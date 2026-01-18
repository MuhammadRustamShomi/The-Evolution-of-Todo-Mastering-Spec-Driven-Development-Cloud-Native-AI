#!/bin/bash
set -e

echo "======================================"
echo "Todo App Deployment Tests"
echo "======================================"

NAMESPACE="todo"
TIMEOUT=60

# Function to check pod status
check_pods() {
    echo "Checking pod status..."
    kubectl get pods -n $NAMESPACE

    # Check all pods are running
    NOT_RUNNING=$(kubectl get pods -n $NAMESPACE --field-selector=status.phase!=Running -o name 2>/dev/null | wc -l)
    if [ "$NOT_RUNNING" -gt 0 ]; then
        echo "Error: Some pods are not running"
        kubectl get pods -n $NAMESPACE --field-selector=status.phase!=Running
        return 1
    fi
    echo "All pods are running!"
}

# Function to test endpoint
test_endpoint() {
    local NAME=$1
    local URL=$2
    local EXPECTED=$3

    echo "Testing $NAME at $URL..."
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$URL" --max-time 10 || echo "000")

    if [ "$RESPONSE" == "$EXPECTED" ]; then
        echo "  $NAME: OK (HTTP $RESPONSE)"
        return 0
    else
        echo "  $NAME: FAILED (Expected HTTP $EXPECTED, got HTTP $RESPONSE)"
        return 1
    fi
}

# Get Minikube IP
MINIKUBE_IP=$(minikube ip 2>/dev/null || echo "localhost")

# Check pods
check_pods

# Wait for ingress to be ready
echo ""
echo "Waiting for ingress to be ready..."
sleep 10

# Test endpoints
echo ""
echo "Testing endpoints..."

ERRORS=0

# Test health endpoints via port-forward (more reliable)
echo "Setting up port forwards..."
kubectl port-forward svc/todo-backend 8000:8000 -n $NAMESPACE &
PF_BACKEND=$!
kubectl port-forward svc/todo-frontend 3000:3000 -n $NAMESPACE &
PF_FRONTEND=$!
sleep 5

test_endpoint "Backend Health" "http://localhost:8000/health" "200" || ((ERRORS++))
test_endpoint "Backend Ready" "http://localhost:8000/ready" "200" || ((ERRORS++))
test_endpoint "Frontend" "http://localhost:3000" "200" || ((ERRORS++))

# Cleanup port forwards
kill $PF_BACKEND $PF_FRONTEND 2>/dev/null || true

# Summary
echo ""
echo "======================================"
if [ $ERRORS -eq 0 ]; then
    echo "All tests passed!"
    exit 0
else
    echo "$ERRORS test(s) failed"
    exit 1
fi
