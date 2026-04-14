from fastapi import FastAPI
import pandas as pd
import mlflow.sklearn
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Identification
NAME = "abelphilipjoseph"
ROLL_NO = "2022bcs0068"

# MLflow Config
TRACKING_URI = os.environ.get("MLFLOW_TRACKING_URI", "http://localhost:5000")
MODEL_NAME = f"{ROLL_NO}_model"
MODEL_STAGE = "Latest" # In Registry terminology, we can use 'latest' or a stage like 'Production'

model = None

@app.on_event("startup")
def load_model():
    global model
    try:
        mlflow.set_tracking_uri(TRACKING_URI)
        # Pulling the latest version of the model from the registry
        model_uri = f"models:/{MODEL_NAME}/latest"
        logger.info(f"Attempting to load model from: {model_uri}")
        model = mlflow.sklearn.load_model(model_uri)
        logger.info("Model loaded successfully from MLflow")
    except Exception as e:
        logger.error(f"Failed to load model from MLflow: {e}")
        logger.info("Falling back to dummy model logic for health check compliance")

@app.get("/")
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "name": NAME,
        "roll_no": ROLL_NO
    }

@app.post("/predict")
def predict(data: dict):
    if model:
        try:
            # Convert input dict to DataFrame
            df = pd.DataFrame([data])
            prediction = model.predict(df)[0]
            result = float(prediction)
        except Exception as e:
            result = f"Error during inference: {str(e)}"
    else:
        result = "Model not loaded"

    return {
        "prediction": result,
        "name": NAME,
        "roll_no": ROLL_NO,
        "input_received": data
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
