from pydantic import BaseModel
from typing import Literal


class MachineInput(BaseModel):
    air_temp: float
    process_temp: float
    rotational_speed: float
    torque: float
    tool_wear: float
    machine_type: Literal["L", "M", "H"]


class PhysicsFeatures(BaseModel):
    power: float
    temp_difference: float
    wear_progression: float


class PredictionResponse(BaseModel):
    prediction: str
    failure_probability: float
    risk_level: str
    recommended_actions: list[str]
    physics_features: PhysicsFeatures
    request_id: str
    timestamp: str