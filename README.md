# LC Credit Risk Underwriting Engine
### PD Modeling (XGBoost) + Qualitative Heuristics (LLM)

## Project Overview
This repository contains a modular decisioning engine designed to evaluate credit risk by synthesizing structured financial data and unstructured applicant intent. 

Unlike traditional "Black Box" models, this system implements a **Hybrid Fusion Layer** that allows for automated qualitative overrides (Vetos) based on employment stability and loan purpose.

## Core Architecture
- **Quantitative Layer:** XGBoost Classifier trained on historical LendingClub data to calculate the **Probability of Default (PD)**.
- **Qualitative Layer:** Llama 3.3 (via Groq LPU) performing sentiment analysis and character risk assessment on 5+ data points.
- **Logic Controller:** A centralized `logic_config` that manages Risk Tolerance Thresholds and Composite Scoring.

## Tech Stack
- **Language:** Python 3.10+
- **Modeling:** XGBoost, Scikit-Learn
- **Inference:** Groq LPU (Low-latency LLM Inference)
- **Deployment:** Hugging Face Spaces (Streamlit SDK)
- **Data Handling:** Pandas, Joblib

## Key Features
- **Deterministic Guardrails:** Quantitative scores are cross-validated against Debt-to-Income (DTI) and Employment Tenure.
- **Dynamic Risk Appetite:** Real-time adjustment of underwriting "strictness" via a centralized configuration.
- **High-Alert UI:** Visual feedback system for immediate risk identification.
