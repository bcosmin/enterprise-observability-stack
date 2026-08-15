.PHONY: help cluster build deploy clean port-forward

# Variables
CLUSTER_NAME ?= observability-cluster
APP_IMAGE ?= demo-python-app:latest

help: ## Show this help message
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

cluster: ## Create a local Kubernetes cluster using Kind
	kind create cluster --name $(CLUSTER_NAME) --config k8s/kind-config.yaml || true

build: ## Build the Python demo application Docker image and load it into Kind
	docker build -t $(APP_IMAGE) ./demo-app
	kind load docker-image $(APP_IMAGE) --name $(CLUSTER_NAME)

deploy: ## Apply all Kubernetes manifests to the observability namespace
	kubectl apply -f k8s/namespace.yaml
	kubectl apply -f k8s/opentelemetry/collector-gateway-config.yaml
	kubectl apply -f k8s/opentelemetry/collector-gateway-deployment.yaml
	kubectl apply -f k8s/backend/loki.yaml
	kubectl apply -f k8s/backend/tempo.yaml
	kubectl apply -f k8s/backend/grafana.yaml
	kubectl apply -f k8s/backend/demo-app-k8s.yaml
	@echo "Deployment complete! Please wait a few seconds for pods to become ready."

port-forward: ## Forward Grafana port to local machine (http://localhost:3000)
	@echo "Access Grafana at http://localhost:3000 (User: admin / Pass: admin)"
	kubectl port-forward -n observability svc/grafana 3000:3000

clean: ## Delete the local Kind cluster and clean up resources
	kind delete cluster --name $(CLUSTER_NAME)