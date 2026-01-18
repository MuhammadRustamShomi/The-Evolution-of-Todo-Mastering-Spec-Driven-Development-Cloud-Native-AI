#!/bin/bash
set -e

echo "======================================"
echo "Todo App Local Kubernetes Deployment"
echo "======================================"

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v minikube &> /dev/null; then
    echo "Error: minikube is not installed"
    exit 1
fi

if ! command -v helm &> /dev/null; then
    echo "Error: helm is not installed"
    exit 1
fi

if ! command -v kubectl &> /dev/null; then
    echo "Error: kubectl is not installed"
    exit 1
fi

# Start minikube if not running
if ! minikube status | grep -q "Running"; then
    echo "Starting minikube..."
    minikube start --cpus=4 --memory=8192 --driver=docker
fi

# Enable ingress addon
echo "Enabling ingress addon..."
minikube addons enable ingress

# Set docker env to use minikube's docker daemon
echo "Configuring Docker to use Minikube..."
eval $(minikube docker-env)

# Build images
echo "Building Docker images..."
cd "$(dirname "$0")/../todo-web"

echo "Building backend..."
docker build -t todo-backend:latest ./backend

echo "Building frontend..."
docker build -t todo-frontend:latest ./frontend

echo "Building AI service..."
docker build -t todo-ai-service:latest ./ai-service

# Update Helm dependencies
echo "Updating Helm dependencies..."
cd "$(dirname "$0")/../charts/todo"
helm dependency update

# Deploy with Helm
echo "Deploying with Helm..."
helm upgrade --install todo . \
    --namespace todo \
    --create-namespace \
    --set backend.image.pullPolicy=Never \
    --set frontend.image.pullPolicy=Never \
    --set aiService.image.pullPolicy=Never \
    --set secrets.openaiApiKey="${OPENAI_API_KEY:-}" \
    --wait --timeout 5m

# Wait for pods
echo "Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/instance=todo -n todo --timeout=300s

# Get ingress IP
echo ""
echo "======================================"
echo "Deployment Complete!"
echo "======================================"
echo ""

MINIKUBE_IP=$(minikube ip)
echo "Add the following to your /etc/hosts file:"
echo "$MINIKUBE_IP  todo.local"
echo ""
echo "Then access the application at: http://todo.local"
echo ""
echo "To view pods: kubectl get pods -n todo"
echo "To view logs: kubectl logs -f deployment/todo-backend -n todo"
