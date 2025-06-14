from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.trace import Status, StatusCode

from random import randint
from flask import Flask, request
import logging

# ----- Tracing Setup -----
resource = Resource(attributes={"service.name": "monolith-analysis-app"})

trace.set_tracer_provider(TracerProvider(resource=resource))
tracer_provider = trace.get_tracer_provider()

otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")
span_processor = BatchSpanProcessor(otlp_exporter)
tracer_provider.add_span_processor(span_processor)

tracer = trace.get_tracer("diceroller.tracer")

# ----- Metrics Setup -----
reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="http://localhost:4318/v1/metrics")
)

metrics.set_meter_provider(MeterProvider(resource=resource, metric_readers=[reader]))
meter = metrics.get_meter("diceroller.meter")

roll_counter = meter.create_counter(
    "dice.rolls",
    description="The number of rolls by roll value",
)

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/")
def roll_dice():
    with tracer.start_as_current_span("roll") as roll_span:
        try:
            player = request.args.get('player', default=None, type=str)
            result = str(roll())
            roll_span.set_attribute("roll.value", result)
            roll_counter.add(1, {"roll.value": result})

            if player:
                logger.warning("%s is rolling the dice: %s", player, result)
            else:
                logger.warning("Anonymous player is rolling the dice: %s", result)

            return result

        except Exception as e:
            roll_span.record_exception(e)
            roll_span.set_status(Status(StatusCode.ERROR))
            logger.exception("An error occurred during dice roll")
            raise

def roll():
    return randint(1, 6)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)