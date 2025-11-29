from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
import os
from config.settings import settings

# Create resource
resource = Resource(attributes={
    "service.name": "research-agent-system",
    "service.version": "1.0.0",
    "deployment.environment": "development"
})

# Set up tracer provider
trace.set_tracer_provider(TracerProvider(resource=resource))

# Configure exporters
otlp_endpoint = settings.otlp_endpoint
if otlp_endpoint:
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=otlp_endpoint))
    )
    print(f"Tracing configured with OTLP endpoint: {otlp_endpoint}")
else:
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(ConsoleSpanExporter())
    )
    print("Tracing configured with console exporter")

# Instrument aiohttp client
AioHttpClientInstrumentor().instrument()

# Get tracer
tracer = trace.get_tracer(__name__)