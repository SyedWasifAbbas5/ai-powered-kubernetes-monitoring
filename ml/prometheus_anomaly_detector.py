import json
import urllib.parse
import urllib.request
import time
import numpy as np
from sklearn.ensemble import IsolationForest

PROMETHEUS_URL = "http://127.0.0.1:9090"

def query_range(query, minutes=5):
    end = int(time.time())
    start = end - (minutes * 60)

    params = urllib.parse.urlencode({
        "query": query,
        "start": start,
        "end": end,
        "step": 15
    })

    url = f"{PROMETHEUS_URL}/api/v1/query_range?{params}"

    with urllib.request.urlopen(url, timeout=10) as response:
        data = json.load(response)

    results = data.get("data", {}).get("result", [])

    values = []

    for result in results:
        for timestamp, value in result.get("values", []):
            try:
                values.append(float(value))
            except (ValueError, TypeError):
                pass

    return values

def detect_anomaly(values):
    if len(values) < 5:
        return {
            "status": "insufficient_data",
            "samples": len(values),
            "message": "Need at least 5 samples for ML analysis."
        }

    values = [float(v) for v in values if np.isfinite(v)]

    if len(values) < 5:
        return {
            "status": "insufficient_data",
            "samples": len(values),
            "message": "Need at least 5 valid samples for ML analysis."
        }

    data = np.array(values).reshape(-1, 1)

    model = IsolationForest(
        contamination=0.2,
        random_state=42
    )

    predictions = model.fit_predict(data)

    anomalies = [
        float(value)
        for value, prediction in zip(values, predictions)
        if prediction == -1
    ]

    return {
        "status": "analyzed",
        "samples": len(values),
        "anomaly_count": len(anomalies),
        "anomalies": anomalies,
        "latest_value": values[-1],
        "min_value": min(values),
        "max_value": max(values)
    }

if __name__ == "__main__":
    print("AI/ML Kubernetes Incident Detection")
    print("===================================")

    latency_query = (
        'rate(app_request_latency_seconds_sum[1m]) '
        '/ rate(app_request_latency_seconds_count[1m])'
    )

    error_query = 'rate(app_errors_total[1m])'

    print("\nQuerying Prometheus historical latency data...")
    latency_values = query_range(latency_query)
    print(f"Latency samples collected: {len(latency_values)}")

    print("\nQuerying Prometheus historical error-rate data...")
    error_values = query_range(error_query)
    print(f"Error-rate samples collected: {len(error_values)}")

    latency_result = detect_anomaly(latency_values)
    error_result = detect_anomaly(error_values)

    print("\n=== LATENCY ML ANALYSIS ===")
    print(json.dumps(latency_result, indent=2))

    print("\n=== ERROR-RATE ML ANALYSIS ===")
    print(json.dumps(error_result, indent=2))

    print("\n=== INCIDENT SUMMARY ===")

    if latency_result["status"] == "analyzed" and latency_result["anomaly_count"] > 0:
        print("WARNING: Abnormal latency detected.")

    if error_result["status"] == "analyzed" and error_result["anomaly_count"] > 0:
        print("WARNING: Abnormal error rate detected.")

    if (
        latency_result.get("anomaly_count", 0) == 0
        and error_result.get("anomaly_count", 0) == 0
    ):
        print("No significant anomalies detected.")
