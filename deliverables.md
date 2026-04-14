# MLOps Assignment Deliverables & Verification
**Student**: abelphilipjoseph | **Roll No**: 2022bcs0068

This document tracks all project requirements and serves as a template for the final PDF report.

---

## ✅ Deliverables Checklist

### Part 1: Problem Definition
- [x] Problem Statement (Wine Quality Regression)
- [x] Dataset Description (Red/White wine features)

### Part 2: Repository Setup
- [x] GitHub Repo: `2022bcs0068-mlops`
- [x] Includes: `train.py`, `main.py`, `Dockerfile`, CI/CD workflow, DVC config.

### Part 3: Data Versioning (DVC + S3)
- [x] DVC Initialized
- [x] S3 Remote Configured (`s3://mlflow-artifacts-2022bcs0068`)
- [x] Two dataset versions (v1: Red, v2: Merged)
- [x] Both versions pushed to S3

### Part 4: CI/CD Pipeline
- [x] GitHub Actions workflow
- [x] Pipeline includes checkout, dependency install, DVC pull, Training, and MLflow logging.

### Part 5: MLflow Tracking (5 Runs)
- [x] Experiment Name: `2022bcs0068_experiment`
- [x] Run 1 (v1, Base Model A)
- [x] Run 2 (v1, Tuned Model A)
- [x] Run 3 (v2, Base Model A)
- [x] Run 4 (v2, Model A + Feature Selection)
- [x] Run 5 (v2, Model B + Feature Selection)
- [x] **Mandatory**: All runs log Name + Roll No.

### Part 6: Model Deployment (FastAPI)
- [x] `/health` returns Name + Roll No
- [x] `/predict` returns Prediction + Name + Roll No

### Part 7: Dockerization
- [x] Image tagged: `iiitkabel/2022bcs0068-mlops`
- [x] Image pushed to Docker Hub

### Part 8: Inference Validation
- [x] Container running on EC2
- [x] Response verified with Name + Roll No

---

## 🖼️ Screenshot Placeholders (Mandatory for Report)

> [!IMPORTANT]
> When taking screenshots, ensure your **Name and Roll Number** are visible in the terminal/UI.

1. **GitHub Repository**: [Screenshot of repository file structure]
2. **DVC + S3**: [Screenshot of `dvc remote list` AND AWS S3 bucket dashboard]
3. **CI/CD Pipeline**: [Screenshot of GitHub Actions tab showing a "Green" success run]
4. **MLflow Dashboard**: [Screenshot of `http://3.91.39.3:5000` showing all 5 runs in a table]
5. **Docker Hub**: [Screenshot of the image repository on hub.docker.com]
6. **EC2 Containers**: [Screenshot of `docker ps` on EC2 showing both API and MLflow containers]
7. **API Validation**: [Screenshot of browser/Postman showing `/health` and `/predict` responses]

---

## 📖 Analysis Questions (Drafted Answers)

### A. Run-Based Analysis
1. **Best Performer**: Run 5 (RandomForest, v2, FS). The ensemble nature of RF handled the merged dataset variance much better than linear ElasticNet.
2. **Dataset Impact**: Merging Red & White (v2) increased initial error (v1 vs v2 base) but allowed more complex models (Run 5) to generalize better.
3. **Hyperparameter Tuning**: Reducing Alpha in ElasticNet (Run 2) improved v1 performance by ~8%, reducing underfitting.
4. **Feature Selection**: Feature selection (Run 4) marginally improved R2 on the broader v2 dataset by removing noisy physicochemical features.
5. **Worst Performer**: Run 3 (v2 Base ElasticNet). The high regularization (Alpha 0.5) was too strict for the merged data complexity.

### B. Experiment Tracking
1. **MLflow Role**: MLflow provided a historical view of every model iteration, allowing us to compare RMSE/R2 side-by-side with parameters.
2. **Useful Info**: The ability to log "Tags" (Name/Roll No) and "Run Name" was most useful for identification and categorization.

### C. Data Versioning
1. **Version Differences**: Version 1 (1599 rows) was purely red wine, while Version 2 (6497 rows) included both, making the task harder but more realistic.
2. **Criticality**: DVC ensures that if we find a bug in Run 1, we can exactly reproduce the data state used at that time, even if the files have changed.

### D. System Design
1. **Reproducibility**: ensured by Git (code) + DVC (data) + GitHub Actions (process) + Docker (environment).
2. **Limitations**: The pipeline currently trains on a small instance; for petabyte-scale data, we would need SageMaker or Spark-ML.
3. **Production Improvement**: Add Prometheus/Grafana for monitoring model drift in production and implement a Model Registry for stage transitions (Staging -> Production).
