# MLOps Pipeline Assignment: Wine Quality Prediction

**Student Name**: abelphilipjoseph  
**Roll Number**: 2022bcs0068  
**Repository Name**: 2022bcs0068-mlops  
**Docker Hub**: [iiitkabel/2022bcs0068-mlops](https://hub.docker.com/r/iiitkabel/2022bcs0068-mlops)

---

## 📖 Project Overview
This project implements an end-to-end MLOps pipeline for predicting wine quality. It satisfies all requirements of the MLOps Pipeline Assignment, including data versioning, experiment tracking, CI/CD, and containerized deployment.

### Problem Statement
- **Type**: Regression
- **Objective**: Predict the quality score (0-10) of wine based on physicochemical properties.
- **Dataset**: UCI Wine Quality Dataset (Red & White versions used).

---

## 🛠️ Tech Stack
- **Data Versioning**: DVC + AWS S3
- **Experiment Tracking**: MLflow
- **CI/CD**: GitHub Actions
- **API Framework**: FastAPI
- **Containerization**: Docker
- **Cloud Infrastructure**: AWS EC2 (Ubuntu 24.04)

---

## 🚀 Setup & Execution

### 1. Local Environment Setup
```bash
# Clone the repository
git clone https://github.com/2022bcs0068-abelphilipjoseph/2022bcs0068-mlops.git
cd 2022bcs0068-mlops

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Data Versioning (DVC)
The data is structured into two explicit versions:
- `v1`: Red Wine (partial)
- `v2`: Merged Red & White Wine (full)

To pull the data from S3:
```bash
dvc pull
```

### 3. Experiment Tracking
Training is performed with MLflow. We conducted 5 mandatory runs with variations in data, hyperparameters, and feature selection.

To view results:
```bash
# If running locally
mlflow ui
# If viewing production
Visit http://<EC2_PUBLIC_IP>:5000
```

### 4. CI/CD Pipeline
Every push to the `master` branch triggers a GitHub Action that:
1. Checks out code
2. Installs dependencies
3. Pulls data from S3 via DVC
4. Trains the model and logs to MLflow
5. Builds and pushes the Docker image to Docker Hub

---

## 🐳 Docker Deployment (EC2)
The production API and MLflow dashboard are hosted on AWS EC2.

### Step 1: Run MLflow Dashboard
```bash
docker run -d --name mlflow-server -p 5000:5000 \
    -e MLFLOW_SERVER_ALLOWED_HOSTS="*" \
    ghcr.io/mlflow/mlflow:v2.10.2 mlflow server --host 0.0.0.0 --port 5000
```

### Step 2: Run FastAPI Model API
```bash
docker pull iiitkabel/2022bcs0068-mlops:latest
docker run -d --name mlops-api -p 80:8000 iiitkabel/2022bcs0068-mlops:latest
```

---

## 🔗 API Endpoints
- **Health Check**: `GET /health` (Returns Name + Roll No)
- **Prediction**: `POST /predict` (Returns Prediction + Name + Roll No)
    - *Example Payload*: `{"fixed acidity": 7.4, "volatile acidity": 0.7}`

---

## 📊 Results Summary
| Run | Dataset | Model | RMSE | R2 |
| :--- | :--- | :--- | :--- | :--- |
| Run 5 | v2 (Full) | RandomForest | 0.657 | 0.415 |

*See `deliverables.md` for full implementation details and analysis.*
