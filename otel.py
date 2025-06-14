from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# Define service name for SigNoz
resource = Resource(attributes={
    "service.name": "monolith-analysis-app"
})

# Set up tracer provider
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

# Set up OTLP exporter to SigNoz
otlp_exporter = OTLPSpanExporter(
    endpoint="http://localhost:4318/v1/traces",  # Default OTLP endpoint for SigNoz
    insecure=True  # Disable TLS (ok for local)
)

# Attach the exporter to the tracer
span_processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(span_processor)

# Create a tracer instance
tracer = trace.get_tracer(__name__)