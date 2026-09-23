#!/usr/bin/env zsh

set -eu

# Check kubeconfig
CURRENT_CONTEXT=$(kubectl config current-context 2>/dev/null || echo "")
if [[ "$CURRENT_CONTEXT" != "minikube" ]]; then
	echo "Please use minikube kubeconfig, got $CURRENT_CONTEXT"
	exit 1
fi

# Start minikube
if ! minikube status >/dev/null 2>&1; then
	echo "Starting minikube..."
	minikube start
else
	echo "Minikube already running"
fi

# Minikube tunnel
if pgrep -f "minikube tunnel" >/dev/null 2>&1; then
	echo "Tunnel already running"
else
	echo "Starting minikube tunnel..."
	minikube tunnel >/dev/null 2>&1 &!
fi

# Func to enable port forwards
forward_port() {
	local namespace=$1
	local service=$2
	local local_port=$3
	local remote_port=$4
	local label=$5

	if lsof -i :$local_port >/dev/null 2>&1; then
	echo "Port $local_port already in use ($label accessible)"
	else
	echo "Forward $label : http://localhost:$local_port"
	kubectl port-forward -n "$namespace" "svc/$service" "$local_port:$remote_port" >/dev/null 2>&1 &!
	fi
}

echo ""
echo "Starting port forwards"
forward_port "app"        "myproject-service" 5000  5000  "Flask API"
forward_port "monitoring" "grafana"           3000  80    "Grafana"
forward_port "app"        "rabbitmq-service"  15672 15672 "RabbitMQ Management"

echo ""
echo "Flask API   : http://localhost:5000"
echo "Grafana     : http://localhost:3000"
echo "RabbitMQ UI : http://localhost:15672"
