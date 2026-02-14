# BuildingMonitor

Small Flask + MySQL project I built while revising backend basics and trying to get closer to the kind of “equipment + telemetry” problems you see in building automation (similar space to Acuity / Atrius).

It’s intentionally a focused proof-of-concept, not a full product.

## What it does

- Register buildings + equipment (HVAC, chillers, elevators, lighting)
- Accept sensor readings (temperature, vibration, runtime hours)
- Flag anomalies using a simple stats baseline
- Auto-updates equipment status: healthy → warning → critical
- Basic PyTest coverage for core endpoints

## Stack

- Python + Flask
- MySQL + SQLAlchemy
- PyTest
- requests (for seeding + sensor simulator)

## Run locally

1) Create `.env` in the project root:

