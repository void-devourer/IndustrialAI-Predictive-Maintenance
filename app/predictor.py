import uuid
import joblib
from pathlib import Path
from datetime import datetime

from app.physics import calculate_physics_features
from app.logger import logger

BASE_DIR = Path(__file__).resolve().parent.parent

artifacts = joblib.load(BASE_DIR / "models" / "artifacts.pkl")

model = artifacts["model"]
thresholds = artifacts["thresholds"]


def predict_machine(data):

    physics = calculate_physics_features(
        data.air_temp,
        data.process_temp,
        data.rotational_speed,
        data.torque,
        data.tool_wear
    )

    type_map = {
        "L": 0,
        "M": 1,
        "H": 2
    }

    features = [[
        type_map[data.machine_type],
        data.air_temp,
        data.process_temp,
        data.rotational_speed,
        data.torque,
        data.tool_wear,
        physics["power"],
        physics["temp_difference"],
        physics["wear_progression"]
    ]]

    prediction = model.predict(features)[0]

    probability = float(model.predict_proba(features)[0][1] * 100)

    # ---------------------------
    # Risk Level
    # ---------------------------

    if probability < 20:
        risk = "LOW"
    elif probability < 50:
        risk = "MODERATE"
    elif probability < 80:
        risk = "HIGH"
    else:
        risk = "CRITICAL"

    # ---------------------------
    # Engineering Recommendations
    # ---------------------------

    recommendations = []

    if physics["power"] > thresholds["power"]:
        recommendations.append(
            "Reduce rotational speed or torque to lower power output."
        )

    if physics["temp_difference"] < thresholds["temp_difference"]:
        recommendations.append(
            "Inspect the cooling system. Heat dissipation appears insufficient."
        )

    if physics["wear_progression"] > thresholds["wear_progression"]:
        recommendations.append(
            "Replace or inspect the cutting tool due to excessive wear."
        )

    if len(recommendations) == 0:
        recommendations.append(
            "Machine is operating within normal operating conditions."
        )

    request_id = str(uuid.uuid4())

    from datetime import datetime, UTC

    timestamp = datetime.now(UTC).isoformat()

    logger.info(
    f"RequestID={request_id} | "
    f"MachineType={data.machine_type} | "
    f"Prediction={'FAILURE' if prediction else 'HEALTHY'} | "
    f"Probability={probability:.2f}% | "
    f"Risk={risk}"
)

    return {
        "prediction": "FAILURE" if prediction else "HEALTHY",
        "failure_probability": round(probability, 2),
        "risk_level": risk,
        "recommended_actions": recommendations,
        "physics_features": physics,
        "request_id": request_id,
        "timestamp": timestamp
    }