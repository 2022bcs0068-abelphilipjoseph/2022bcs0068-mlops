from fastapi import FastAPI
import pandas as pd
import mlflow.sklearn
import os

app = FastAPI()

# Identification
NAME = "abelphilipjoseph"
ROLL_NO = "2022bcs0068"

# Load the best model (placeholder for now, will be updated by CI/CD or local runs)
# In production, we might pull from MLflow or a specific path
MODEL_PATH = "model" # This will be where the logged model is stored/downloaded

@app.get("/")
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "name": NAME,
        "roll_no": ROLL_NO
    }

@app.post("/predict")
def predict(data: dict):
    # This is a simplified prediction endpoint
    # In a real scenario, we'd load the model and run inference
    # For the assignment, we need to return high-level structure
    
    # Placeholder prediction logic
    # model = mlflow.sklearn.load_model(MODEL_PATH)
    # prediction = model.predict(pd.DataFrame([data]))[0]
    
    return {
        "prediction": "Model prediction would be here",
        "name": NAME,
        "roll_no": ROLL_NO,
        "input_received": data
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
