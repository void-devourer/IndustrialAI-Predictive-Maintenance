from fastapi import FastAPI
from app.crud import save_prediction, get_all_predictions
from app.models import create_tables
from app.schemas import MachineInput
from app.predictor import predict_machine


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

    result = predict_machine(data)

    physics = result["physics_features"]

    save_prediction(
        result=result,
        data=data,
        physics=physics
    )

    return result


@app.get("/history")
def history():

    return get_all_predictions()