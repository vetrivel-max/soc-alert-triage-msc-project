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