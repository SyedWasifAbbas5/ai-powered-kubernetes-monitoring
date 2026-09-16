import json
import subprocess
import sys
from pathlib import Path

def run_detector():
    result = subprocess.run(
        [sys.executable, "ml/prometheus_anomaly_detector.py"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(result.stderr)
        sys.exit(result.returncode)

    return result.stdout

def classify_incident(text):
    text_lower = text.lower()

    if "abnormal latency detected" in text_lower and "abnormal error rate detected" in text_lower:
        return {
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

    if "abnormal latency detected" in text_lower:
        return {
            "incident": "HIGH_LATENCY",
            "severity": "MEDIUM",
            "cause": "Application response latency is significantly above the normal baseline",
            "actions": [
                "kubectl top pods -n ai-monitoring",
                "kubectl logs -n ai-monitoring -l app=ai-monitoring-app --tail=100",
                "Inspect application dependencies and slow requests",
                "Review Grafana latency metrics"
            ]
        }

    if "abnormal error rate detected" in text_lower:
        return {
            "incident": "HIGH_ERROR_RATE",
            "severity": "HIGH",
            "cause": "Application error rate is above the learned baseline",
            "actions": [
                "kubectl logs -n ai-monitoring -l app=ai-monitoring-app --tail=100",
                "kubectl describe pods -n ai-monitoring",
                "Check recent deployments",
                "Review application health and dependencies",
                "Inspect Grafana error metrics"
            ]
        }

    return {
        "incident": "NO_ANOMALY",
        "severity": "NORMAL",
        "cause": "No significant anomaly detected",
        "actions": [
            "Continue monitoring application metrics"
        ]
    }

print("AI/ML Kubernetes Incident Response")
print("==================================")

detector_output = run_detector()

print(detector_output)

diagnosis = classify_incident(detector_output)

print("=== INCIDENT ASSISTANT ===")
print(json.dumps(diagnosis, indent=2))

Path("incident-report.json").write_text(
    json.dumps(diagnosis, indent=2)
)

print("\nIncident report written to incident-report.json")
