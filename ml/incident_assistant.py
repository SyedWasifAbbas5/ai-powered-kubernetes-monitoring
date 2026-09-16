from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

training_text = [
    "pod cpu usage is extremely high",
    "container cpu spike",
    "high cpu utilization",
    "pod memory usage is extremely high",
    "memory pressure out of memory",
    "container ran out of memory",
    "pod is crashloopbackoff",
    "container keeps restarting",
    "application container crashes",
    "readiness probe failed",
    "liveness probe failed",
    "pod is not ready",
    "connection timeout network error",
    "service cannot connect",
    "network connection refused"
]

labels = [
    "CPU_SPIKE", "CPU_SPIKE", "CPU_SPIKE",
    "MEMORY_PRESSURE", "MEMORY_PRESSURE", "MEMORY_PRESSURE",
    "CRASH_LOOP", "CRASH_LOOP", "CRASH_LOOP",
    "HEALTH_CHECK_FAILURE", "HEALTH_CHECK_FAILURE", "HEALTH_CHECK_FAILURE",
    "NETWORK_FAILURE", "NETWORK_FAILURE", "NETWORK_FAILURE"
]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(training_text)

model = LogisticRegression(max_iter=1000)
model.fit(X, labels)

remediation = {
    "CPU_SPIKE": "Check kubectl top pods, inspect CPU limits and investigate high-load requests.",
    "MEMORY_PRESSURE": "Check memory usage, pod limits and recent application changes.",
    "CRASH_LOOP": "Inspect kubectl logs and describe the pod to identify startup or runtime failures.",
    "HEALTH_CHECK_FAILURE": "Inspect readiness/liveness probes and verify application health endpoints.",
    "NETWORK_FAILURE": "Check Kubernetes Service, endpoints, DNS resolution and NetworkPolicies."
}

def analyze_incident(text):
    prediction = model.predict(vectorizer.transform([text]))[0]
    confidence = max(model.predict_proba(vectorizer.transform([text]))[0])

    return {
        "incident_type": prediction,
        "confidence": round(float(confidence), 3),
        "recommended_action": remediation[prediction]
    }

if __name__ == "__main__":
    examples = [
        "pod cpu usage suddenly increased",
        "application pod keeps restarting",
        "readiness probe failed repeatedly"
    ]

    for example in examples:
        print("\nIncident:", example)
        print(analyze_incident(example))
