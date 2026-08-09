from fastapi import FastAPI

from app.crud import save_prediction, get_all_predictions
from app.models import create_tables
from app.schemas import MachineInput
from app.predictor import predict_machine
from app.rag import retrieve_knowledge
from app.llm import generate_maintenance_explanation


app = FastAPI(title="Industrial AI Monitoring Platform")


@app.on_event("startup")
def startup():
    create_tables()


@app.get("/")
def home():
    return {
        "message": "Industrial AI Monitoring Platform Running"
    }


@app.post("/predict")
def predict(data: MachineInput):

    # 1. Run machine-learning prediction
    result = predict_machine(data)

    physics = result["physics_features"]

    # 2. Build a query from the prediction and machine conditions
    query = (
        f"{result['prediction']} "
        f"{result['risk_level']} "
        f"torque "
        f"rotational speed "
        f"tool wear "
        f"temperature"
    )

    # 3. Retrieve relevant maintenance knowledge
    knowledge = retrieve_knowledge(query)

    # 4. Generate AI explanation using retrieved knowledge
    ai_explanation = generate_maintenance_explanation(
        prediction=result["prediction"],
        probability=result["failure_probability"],
        risk_level=result["risk_level"],
        machine_data={
            "air_temp": data.air_temp,
            "process_temp": data.process_temp,
            "rotational_speed": data.rotational_speed,
            "torque": data.torque,
            "tool_wear": data.tool_wear,
            "machine_type": data.machine_type,
        },
        retrieved_knowledge=knowledge,
    )

    # 5. Add AI explanation to the response
    result["ai_explanation"] = ai_explanation

    # 6. Save prediction to PostgreSQL
    save_prediction(
        result=result,
        data=data,
        physics=physics
    )

    # 7. Return complete result to Streamlit
    return result


@app.get("/history")
def history():
    return get_all_predictions()