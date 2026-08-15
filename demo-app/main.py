import time
import random
import logging
from fastapi import FastAPI, Response, status
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# 1. OpenTelemetry Resource Configuration
resource = Resource.create(attributes={"service.name": "demo-python-app", "environment": "production"})

# Traces Configuration
trace_provider = TracerProvider(resource=resource)
otlp_trace_exporter = OTLPSpanExporter(endpoint="otel-collector-gateway.observability.svc.cluster.local:4317", insecure=True)
trace_provider.add_span_processor(BatchSpanProcessor(otlp_trace_exporter))
trace.set_tracer_provider(trace_provider)
tracer = trace.get_tracer("demo-tracer")

# Metrics Configuration
metric_provider = MeterProvider(resource=resource)
metrics.set_meter_provider(metric_provider)
meter = metrics.get_meter("demo-meter")
request_counter = meter.create_counter(
    name="app_requests_total",
    description="Total number of requests received",
    unit="1"
)

# Logging Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("demo-app")

app = FastAPI(title="Demo Observability App")

@app.get("/")
def read_root():
    request_counter.add(1, {"endpoint": "/", "status": "200"})
    logger.info("Root endpoint called successfully.")
    return {"message": "Hello from Enterprise Observability Stack!"}

@app.get("/process")
def process_task(response: Response):
    # Simulare latență aleatorie
    latency = random.uniform(0.1, 0.8)
    time.sleep(latency)
    
    # Error simulation: 20% chance of failure
    if random.random() < 0.2:
        request_counter.add(1, {"endpoint": "/process", "status": "500"})
        logger.error("Internal processing failed due to a simulated database error.")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": "Simulated internal server error"}

    request_counter.add(1, {"endpoint": "/process", "status": "200"})
    logger.info(f"Task processed successfully in {latency:.2f}s")
    return {"status": "success", "processing_time_seconds": round(latency, 2)}

# Instrument the FastAPI app with OpenTelemetry
FastAPIInstrumentor.instrument_app(app)