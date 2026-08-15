# Enterprise Observability Stack

A production-ready, vendor-agnostic Observability Stack built on cloud-native standards. This project demonstrates how to implement a unified observability pipeline using **OpenTelemetry**, **Loki** (logs), **Tempo** (traces), **Mimir/Prometheus** (metrics), and **Grafana** (visualization).

## Architecture Overview
This stack follows the modern **LGTM** (Loki, Grafana, Tempo, Mimir/Prometheus) pattern, standardized by OpenTelemetry.

*   **Telemetry Collection:** OpenTelemetry Collector (Gateway) acts as the central hub for all signals.
*   **Storage Backend:**
    *   **Metrics:** VictoriaMetrics/Mimir for high-scale time-series data.
    *   **Traces:** Grafana Tempo for cost-effective distributed tracing.
    *   **Logs:** Grafana Loki for label-based log aggregation.
*   **Visualization:** Grafana as the unified pane of glass, featuring correlated views (Trace-to-Logs-to-Metrics).
*   **Demo Application:** A Python/FastAPI microservice instrumented with OpenTelemetry SDKs, generating simulated traffic, latency, and errors.

## Prerequisites
- [Docker](https://www.docker.com/)
- [Kind](https://kind.sigs.k8s.io/) (Kubernetes in Docker)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- make

## Getting Started

### 1. Provision Cluster & Build
```bash
# Create the Kind cluster
make cluster

# Build and load the demo application
make build
```

### 2. Deploy the Stack
```bash
# Deploy the stack
make deploy
```

### 3. Access the Dashboard
```bash
# Forward Grafana to localhost:3000
make port-forward
```
- **URL:** http://localhost:3000
- **Credentials:** admin / admin

## Project Structure
```plaintext
enterprise-observability-stack/
├── Makefile                # Automated deployment commands
├── k8s/                    # Kubernetes manifests
│   ├── opentelemetry/      # OTel Gateway configuration
│   ├── backend/            # LGTM component configurations
│   └── namespace.yaml      # Environment isolation
├── demo-app/               # Instrumented Python microservice
└── README.md
```