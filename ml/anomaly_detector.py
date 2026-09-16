import numpy as np
from sklearn.ensemble import IsolationForest

def detect_anomalies(values):
    data = np.array(values).reshape(-1, 1)

    model = IsolationForest(
        contamination=0.1,
        random_state=42
    )

    predictions = model.fit_predict(data)

    return [
        {
            "value": float(value),
            "anomaly": prediction == -1
        }
        for value, prediction in zip(values, predictions)
    ]

if __name__ == "__main__":
    baseline = [20, 21, 19, 22, 20, 21, 23, 19, 22, 21]
    incident = [20, 21, 22, 95, 21, 20, 110, 22, 21]

    values = baseline + incident

    print("ML Kubernetes Metric Anomaly Detection")
    print("---------------------------------------")

    for result in detect_anomalies(values):
        status = "ANOMALY" if result["anomaly"] else "normal"
        print(f"value={result['value']:6.1f} -> {status}")
