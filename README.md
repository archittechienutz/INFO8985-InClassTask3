## README - Monolith Analysis App with OpenTelemetry
## Overview
This is a Flask-based web application that simulates a dice roll and integrates monitoring and observability features using OpenTelemetry. 
The application exports tracing and metric data to SigNoz for observability and debugging.

## Features

- Endpoint `/rolldice` (or `/`) to simulate dice rolls
- OpenTelemetry Tracing and Metrics setup
- Exception logging for simulated failures
- Integration with SigNoz (OTLP over HTTP)

## Prerequisites

- Python 3.12+
- Flask
- opentelemetry-api
- opentelemetry-sdk
- opentelemetry-exporter-otlp
- SigNoz running locally (default endpoint http://localhost:4318)

## Installation & Setup

1. Clone the repository.
2. Install the required dependencies:
   pip install flask opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp
3. Ensure SigNoz is running (use Docker or install manually).
4. Run the Flask application:
   python app.py

## Usage

- Navigate to http://localhost:3000/ (or /rolldice if that's your route).
- Optional: Use `?player=name` to simulate a player rolling the dice.
- Check SigNoz UI (http://localhost:3301) for traces and metrics.

## Testing Exceptions

To simulate an error and test trace exceptions in SigNoz, modify the `roll()` function to:
    raise Exception("Simulated dice roll failure!")
Then hit the endpoint to trigger the error and view the trace in SigNoz.
