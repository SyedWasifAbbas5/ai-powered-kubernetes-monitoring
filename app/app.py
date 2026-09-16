from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import os, time, random

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total application requests",
    ["endpoint", "method", "status"]
)

REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds",
    "Application request latency",
    ["endpoint"]
)

ERROR_COUNT = Counter(
    "app_errors_total",
    "Total application errors"
)

@app.before_request
def start_timer():
    from flask import g
    g.start_time = time.time()

@app.after_request
def record_metrics(response):
    from flask import request, g
    latency = time.time() - g.start_time
    REQUEST_COUNT.labels(request.path, request.method, response.status_code).inc()
    REQUEST_LATENCY.labels(request.path).observe(latency)
    return response

@app.route("/")
def home():
    return jsonify({
        "application": "ai-powered-kubernetes-monitoring",
        "version": "1.0.0",
        "status": "running",
        "message": "AI/ML Kubernetes monitoring platform"
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

@app.route("/simulate/error")
def simulate_error():
    ERROR_COUNT.inc()
    REQUEST_COUNT.labels("/simulate/error", "GET", 500).inc()
    return jsonify({
        "status": "error",
        "message": "Simulated application failure"
    }), 500

@app.route("/simulate/latency")
def simulate_latency():
    delay = random.uniform(2, 5)
    time.sleep(delay)
    return jsonify({
        "status": "slow",
        "delay_seconds": round(delay, 2)
    })

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
