from flask import Flask, request, render_template
from flask_sock import Sock
import time
import asyncio
import psutil
import numpy as np
import logging
from prometheus_client import make_wsgi_app, Counter, Histogram
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import time
import requests
from opentelemetry import metrics
from opentelemetry import trace 
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
        OTLPMetricExporter,
    )

from opentelemetry.sdk.metrics.export import (
    PeriodicExportingMetricReader,
)

tracer = trace.get_tracer("__name__")
metric_reader = PeriodicExportingMetricReader(OTLPMetricExporter())
provider = MeterProvider(metric_readers=[metric_reader])
# Sets the global default meter provider
metrics.set_meter_provider(provider)
# Creates a meter from the global meter provider, the metrics are named "cf_request.counter" and "cf_latency.histo"
meter = metrics.get_meter("my.meter.name")
cf_request_count = meter.create_counter(name="cf_request.counter", unit="1", description="Counter type metric type")
cf_request_latency = meter.create_histogram(name="cf_latency.histo", unit="s")

app = Flask(__name__)
sock = Sock(app)

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

REQUEST_COUNT = Counter(
    'pyapp_local_request_count',
    'Application Request Count',
    ['method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'pyapp_local_request_latency_seconds',
    'Application Request Latency',
    ['method', 'endpoint']
)


class HealthRequestFilter(logging.Filter):
    def filter(self, record):
        # Exclude log records for /health requests
        return 'health' not in record.getMessage() and 'metrics' not in record.getMessage()

# Create a logger and add the custom filter to it
logger = logging.getLogger('werkzeug')
# logger.addFilter(HealthRequestFilter())

@app.route('/')
def hello():
    with tracer.start_as_current_span("cf-/") as span:
        start_time = time.time()
        REQUEST_COUNT.labels('GET', '/', 200).inc()
    # getting a counter  metric via Otel native
        cf_request_count.add(1, {
            "method": request.method,
            "endpoint": request.endpoint,
        });
        template = render_template('index.html')
        REQUEST_LATENCY.labels('GET', '/').observe(time.time() - start_time)
    # getting a histogram  metric via Otel native
        cf_request_latency.record((time.time() - start_time), {
            "method": request.method,
            "endpoint": request.endpoint})
        return template


@app.route('/health')
def health():
    cf_request_count.add(1, {
        "method": request.method,
        "endpoint": request.endpoint,
    });    
    return "OK";


@app.route('/submit', methods=['POST'])
def submit():
    start_time = time.time()

    # Simulate processing submitted data
    data = request.get_json()
    app.logger.info(f"Received data: {data}")
    time.sleep(0.5)  # simulate work

    REQUEST_COUNT.labels('POST', '/submit', 201).inc()
    # getting a counter  metric via Otel native
    cf_request_count.add(1, {
        "method": request.method,
        "endpoint": request.endpoint,
    });


    REQUEST_LATENCY.labels('POST', '/submit').observe(time.time() - start_time)
    # getting a histogram  metric via Otel native
    cf_request_latency.record((time.time() - start_time), {
        "method": request.method,
        "endpoint": request.endpoint})
    with tracer.start_as_current_span(
        "cf-submit", 
        ):

        return {"cf_body": data}, 201
        # app.logger.info(f"Payload value: {data}")


@app.route('/resource/<int:id>', methods=['DELETE'])
def delete_resource(id):
    start_time = time.time()

    # Simulate deletion of a resource
    app.logger.info(f"Deleting resource with ID: {id}")
    time.sleep(0.2)  # simulate work

    REQUEST_COUNT.labels('DELETE', '/resource', 204).inc()
    # getting a counter  metric via Otel native
    cf_request_count.add(1, {
        "method": request.method,
        "endpoint": request.endpoint,
    });    
    REQUEST_LATENCY.labels('DELETE', '/resource').observe(time.time() - start_time)
    # getting a histogram  metric via Otel native
    cf_request_latency.record((time.time() - start_time), {
        "method": request.method,
        "endpoint": request.endpoint})

    return '', 204

# the debug parameter here was creating the original issue
# https://opentelemetry.io/docs/zero-code/python/troubleshooting/#flask-debug-mode-with-reloader-breaks-instrumentation
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
