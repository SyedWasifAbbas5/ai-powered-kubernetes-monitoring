# AI-Powered Kubernetes Monitoring & Incident Response

An AI/ML-powered Kubernetes monitoring platform that analyzes Prometheus metrics, detects abnormal application behavior and generates automated incident-response guidance for engineers.

## Architecture

```text
                    Kubernetes
                        │
                        ▼
              ┌──────────────────┐
              │ Flask Application │
              └────────┬─────────┘
                       │
                       ▼
                 Prometheus
                       │
                       ▼
              Historical Metrics
                       │
                       ▼
            Isolation Forest (ML)
                       │
              ┌────────┴────────┐
              │                 │
          Anomaly           Normal
              │                 │
              ▼                 ▼
       Incident Assistant    No Alert
              │
              ▼
       Incident Classification
              │
              ▼
     Probable Cause + Actions
              │
              ▼
           Engineer
```

## Project Overview

This project demonstrates how AI/ML can be integrated into a Kubernetes observability workflow.

The platform:

* Runs a containerized Flask application on Kubernetes
* Exposes Prometheus application metrics
* Collects historical metrics with Prometheus
* Visualizes metrics through Grafana
* Uses Isolation Forest for metric anomaly detection
* Detects abnormal latency and application error rates
* Classifies detected incidents
* Generates troubleshooting recommendations
* Produces a machine-readable incident report

The implementation is designed to run locally using Kubernetes Kind and does not require paid cloud services or GPUs.

## Key Features

### Kubernetes Monitoring

* Kubernetes Deployment
* Kubernetes Service
* Health and readiness probes
* Resource requests and limits
* Non-root container execution
* Prometheus metrics endpoint

### Prometheus

The application exposes metrics including:

```text
app_requests_total
app_errors_total
app_request_latency_seconds
```

Prometheus collects these metrics at regular intervals and provides historical data for analysis.

### Grafana Dashboard

The Grafana dashboard provides visibility into:

* Application Requests
* Application Error Rate
* Application Request Latency

Prometheus is configured as the Grafana data source.

### ML Anomaly Detection

The project uses:

```text
scikit-learn
IsolationForest
```

The ML detector analyzes historical Prometheus data rather than relying only on static thresholds.

Example latency analysis:

```text
Latency samples collected: 78
Valid samples: 63
Anomalies detected: 13
Maximum observed latency: ~7.17 seconds
```

Example error-rate analysis:

```text
Error-rate samples collected: 21
Anomalies detected: 3
Latest error rate: ~0.156
```

The exact results vary depending on the generated traffic and Prometheus history.

## AI/ML Incident Assistant

When abnormal behavior is detected, the incident-response component classifies the event.

Example:

```json
{
  "incident": "APPLICATION_DEGRADATION",
  "severity": "HIGH",
  "cause": "Elevated request latency combined with increased application errors",
  "actions": [
    "kubectl get pods -n ai-monitoring",
    "kubectl describe pods -n ai-monitoring",
    "kubectl logs -n ai-monitoring -l app=ai-monitoring-app --tail=100",
    "Check recent application deployments and configuration changes",
    "Inspect Prometheus and Grafana metrics for continued degradation"
  ]
}
```

The recommendations are intended to help an engineer move from anomaly detection to practical Kubernetes troubleshooting.

## Simulated Incidents

The application includes endpoints for generating test conditions.

### Application Error

```text
/simulate/error
```

Generates an application error and increments the error counter.

### Application Latency

```text
/simulate/latency
```

Introduces artificial request latency between approximately 2–5 seconds.

These endpoints make it possible to generate realistic monitoring data without requiring an actual production failure.

## Repository Structure

```text
.
├── app/
│   ├── app.py
│   └── requirements.txt
│
├── k8s/
│   ├── deployment.yaml
│   ├── namespace.yaml
│   ├── service.yaml
│   └── servicemonitor.yaml
│
├── ml/
│   ├── anomaly_detector.py
│   ├── incident_assistant.py
│   └── incident_response.py
│
├── monitoring/
│   ├── prometheus.yaml
│   └── grafana.yaml
│
├── Dockerfile
├── incident-report.json
├── .dockerignore
└── README.md
```

## Technologies

* Kubernetes
* Kind
* Docker
* Python
* Flask
* Prometheus
* Grafana
* scikit-learn
* NumPy
* GitHub
* Linux
* YAML

## Local Deployment

Create the Kubernetes cluster:

```bash
kind create cluster --name ai-monitoring
```

Create the application namespace:

```bash
kubectl apply -f k8s/namespace.yaml
```

Build the application image:

```bash
docker build -t ai-monitoring-app:1.0.0 .
```

Load the image into Kind:

```bash
kind load docker-image ai-monitoring-app:1.0.0 --name ai-monitoring
```

Deploy the application:

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

Deploy monitoring:

```bash
kubectl create namespace monitoring
kubectl apply -f monitoring/prometheus.yaml
kubectl apply -f monitoring/grafana.yaml
```

Verify the workloads:

```bash
kubectl get pods -n ai-monitoring
kubectl get pods -n monitoring
```

## Access Prometheus

```bash
kubectl -n monitoring port-forward svc/prometheus 9090:9090
```

Open:

```text
http://localhost:9090
```

Example PromQL:

```promql
app_requests_total
```

```promql
rate(app_errors_total[1m])
```

Average request latency:

```promql
rate(app_request_latency_seconds_sum[1m])
/
rate(app_request_latency_seconds_count[1m])
```

## Access Grafana

```bash
kubectl -n monitoring port-forward svc/grafana 3000:3000
```

Open:

```text
http://localhost:3000
```

Default local credentials:

```text
Username: admin
Password: admin
```

Prometheus data source:

```text
http://prometheus.monitoring.svc.cluster.local:9090
```

## Run ML Anomaly Detection

With Prometheus available on localhost:

```bash
python ml/prometheus_anomaly_detector.py
```

The detector queries historical Prometheus data and evaluates the collected values using Isolation Forest.

## Run Incident Response

```bash
python ml/incident_response.py
```

The script:

1. Queries Prometheus
2. Detects metric anomalies
3. Determines whether an incident exists
4. Classifies the incident
5. Assigns a severity
6. Generates troubleshooting recommendations
7. Writes `incident-report.json`

## Incident Workflow

```text
Application Traffic
        ↓
Prometheus Metrics
        ↓
Historical Metric Data
        ↓
Isolation Forest
        ↓
Anomaly Detection
        ↓
Incident Classification
        ↓
AI/ML Incident Assistant
        ↓
Probable Cause
        ↓
Kubernetes Troubleshooting Actions
```

## Production Engineering Concepts Demonstrated

This project demonstrates practical concepts used in modern DevOps and SRE environments:

* Kubernetes observability
* Application metrics
* Prometheus monitoring
* Grafana visualization
* Historical time-series analysis
* ML-based anomaly detection
* Incident classification
* Automated troubleshooting guidance
* Container security
* Kubernetes health checks
* Resource management
* Production incident simulation

## Important Implementation Note

The project uses a lightweight local ML approach rather than a paid external LLM or GPU-based model.

The anomaly detection layer uses **Isolation Forest**, while the incident assistant uses a lightweight classification approach and predefined remediation knowledge.

This keeps the project reproducible in a free development environment while demonstrating the core AI-assisted observability workflow.

## Portfolio Value

This project demonstrates the integration of:

**DevOps + Kubernetes + Observability + Python + Machine Learning + Incident Response**

It goes beyond basic Kubernetes deployment by showing how historical monitoring data can be analyzed automatically and converted into actionable troubleshooting guidance.

## Author

**Syed Wasif Abbas**
