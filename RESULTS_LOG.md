# Project Results Log

## Stage 1 Model (CICIDS2017) — Normal vs Attack
- Overall Accuracy: 99.89%
- Missed attacks (false negatives): 93
- False alarms (false positives): 484
- Training time: 135.96 seconds
- Dataset: 2,520,798 cleaned rows (2,095,057 Normal / 425,741 Attack)

## Stage 2 Model (CICIDS2017) — Attack Type Classification
- Overall Accuracy: 99.94% (after merging Web Attack subtypes)
- Before merge: 99.75% (SQL Injection had 0% precision/recall)
- 12 attack categories after merge

## SMOTE Experiment (negative result, honestly reported)
- Missed attacks increased from 93 to 109 after SMOTE oversampling
- Conclusion: synthetic oversampling on extremely rare classes (Bot) introduced unrealistic patterns

## Own Live-Lab Model (NFStream, self-generated traffic)
- Overall Accuracy: 99.97%
- Trained on 236,629 flows (DoS, PortScan, BruteForce, Normal)
- Captured via Kali VM attacking Metasploitable
- Normal traffic precision: 86% (documented limitation — only 400 Normal samples)

## Live Real-Time Pipeline
- NFStream live capture on Kali eth0
- Predictions served via Flask, refreshing every 3 seconds
- Confirmed working end-to-end: attack traffic generated on Kali → classified within seconds → shown on dashboard

## Model Comparison (Random Forest vs Logistic Regression vs XGBoost)
- Compared on identical Stage 1 train/test split
- Logistic Regression: 88.03% accuracy, 60.27% precision, 85.50% recall, 70.70% F1 (543.55s training time)
- Random Forest: 99.89% accuracy, 99.43% precision, 99.89% recall, 99.66% F1
- XGBoost: 99.92% accuracy, 99.65% precision, 99.85% recall, 99.75% F1 (25.30s training time — fastest and slightly best)
- Conclusion: Random Forest retained as primary model for SHAP compatibility; XGBoost validated as a strong, faster alternative; Logistic Regression confirms the problem is not linearly separable

## Dashboard Features Added
- Alert stats summary panels (Total/Attack/Normal/Risk breakdown) on all 3 alert dashboards
- Model Comparison dashboard page (/model-comparison) with Chart.js bar chart visualization
- Search/filter (Src/Dst IP, status, risk level) on Own Model and Live Feed dashboards
- CSV export button on all 3 alert dashboards
- 4-level risk system (Critical/High/Medium/Low) for own-lab model, with confidence-based downgrade (predictions under 60% confidence drop one risk level)
- Consistent navigation bar with active-page highlighting across all 4 dashboard views

## Evidence Collected
- Screenshots of all 4 dashboards (Static, Own Model, Live Feed, Model Comparison)
- Screen-recorded video of live attack detection (Nmap scan against Metasploitable, detected and shown on Live Feed dashboard within seconds)
- Full codebase backed up to private GitHub repository