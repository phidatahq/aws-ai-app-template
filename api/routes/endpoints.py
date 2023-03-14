from dataclasses import dataclass


@dataclass
class ApiEndpoints:
    PING: str = "/ping"
    HEALTH: str = "/health"
    PREDICT: str = "/predict"


endpoints = ApiEndpoints()
