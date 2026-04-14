import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_squared_error, r2_score
import mlflow
import mlflow.sklearn
import argparse
import os

# Identification
NAME = "abelphilipjoseph"
ROLL_NO = "2022bcs0068"

def train_model(data_path, model_type, alpha, l1_ratio, n_estimators, feature_selection):
    # Set remote tracking URI if available
    tracking_uri = os.environ.get("MLFLOW_TRACKING_URI")
    if tracking_uri:
        mlflow.set_tracking_uri(tracking_uri)
        print(f"Tracking to: {tracking_uri}")

    # Set experiment
    mlflow.set_experiment(f"{ROLL_NO}_experiment")
    
    with mlflow.start_run() as run:
        # Read dataset
        print(f"Active Run ID: {run.info.run_id}")
        df = pd.read_csv(data_path)
        
        # Identification suffix in logs
        mlflow.set_tag("student_name", NAME)
        mlflow.set_tag("roll_no", ROLL_NO)
        mlflow.set_tag("model_type", model_type)
        
        # Feature Selection
        if feature_selection:
            # Example: Use only top 5 correlated features with quality
            corr = df.corr()
            top_features = corr['quality'].abs().sort_values(ascending=False).index[1:6]
            X = df[top_features]
            mlflow.log_param("features_used", list(top_features))
        else:
            X = df.drop(columns=['quality'])
            mlflow.log_param("features_used", "all")

        y = df['quality']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Log params
        mlflow.log_param("dataset_version", "v1" if "v1" in data_path else "v2")
        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_param("n_estimators", n_estimators)

        # Select Model
        if model_type == "RandomForest":
            model = RandomForestRegressor(n_estimators=n_estimators, random_state=42)
        else:
            model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
        
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        
        # Metrics
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        r2 = r2_score(y_test, predictions)
        
        print(f"Model: {model_type}, Dataset: {data_path}, RMSE: {rmse}, R2: {r2}")
        
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        
        # Name + Roll No in metrics artifact
        metrics = {
            "rmse": rmse,
            "r2": r2,
            "name": NAME,
            "roll_no": ROLL_NO
        }
        # Log metrics to MLflow
        mlflow.log_dict(metrics, "metrics.json")
        
        # Also write local metrics.json for GitHub Actions summary
        import json
        with open("metrics.json", "w") as f:
            json.dump(metrics, f, indent=4)
        print("Successfully wrote metrics.json")
        
        # Log and Register model
        # Using a consistent name to allow the API to 'Pull the latest best'
        model_name = f"{ROLL_NO}_model"
        mlflow.sklearn.log_model(
            sk_model=model, 
            artifact_path="model",
            registered_model_name=model_name
        )
        print(f"Model registered as: {model_name}")

        # Also save locally for GitHub Artifact upload (as per template)
        os.makedirs("models", exist_ok=True)
        import joblib
        joblib.dump(model, "models/model.pkl")
        print("Model saved locally to models/model.pkl")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, default="data/winequality.csv")
    parser.add_argument("--model", type=str, default="ElasticNet")
    parser.add_argument("--alpha", type=float, default=0.5)
    parser.add_argument("--l1_ratio", type=float, default=0.5)
    parser.add_argument("--n_estimators", type=int, default=100)
    parser.add_argument("--feature_selection", action="store_true")
    
    args = parser.parse_args()
    
    train_model(args.data, args.model, args.alpha, args.l1_ratio, args.n_estimators, args.feature_selection)
