# HDI Insight AI – Smart Human Development Analytics Platform

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask Version](https://img.shields.io/badge/Flask-2.2%2B-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Production-Ready](https://img.shields.io/badge/Status-Production--Ready-brightgreen.svg)]()

HDI Insight AI is a premium, portfolio-ready web analytics application that uses machine learning to predict the **Human Development Index (HDI)** category of a country in real-time. It incorporates interactive visualizations, explainable AI diagnostics, dynamic policy recommendations, and client-side report generators.

---

## 📸 Screenshots

A complete gallery of visual walkthroughs is saved in the [Screenshots/](Screenshots/) directory.
* **Dashboard Analytics View**: [Screenshots/Dashboard.png](Screenshots/Dashboard.png)
* **Live Simulator Interface**: [Screenshots/Prediction.png](Screenshots/Prediction.png)
* **Model Performance Suite**: [Screenshots/ModelPerformance.png](Screenshots/ModelPerformance.png)

---

## 🛠 Technology Stack

* **Backend Framework**: Python, Flask (routing and microservices)
* **Machine Learning Pipeline**: Scikit-learn (SVM RBF, Random Forest, scaling parameters)
* **Database Engine**: SQLite3 (persistent prediction histories)
* **Data Processing**: Pandas, NumPy
* **Frontend Design**: Vanilla HTML5, CSS3 Variables (theme switching), ES6 JavaScript
* **Reporting Engine**: ReportLab (dynamic PDF generation)

---

## 🧠 Machine Learning Workflow

```
Raw Data (UNDP/World Bank)
  ↓
Clean & Handle Missing Values (Median Imputation)
  ↓
Log Transformation (GNI Per Capita Scale Alignment)
  ↓
Feature Centering & Scaling (StandardScaler)
  ↓
Classification & Regression Inference (SVM & Random Forest)
  ↓
Explainable AI (Feature Strengths) & Advisory Rules (Recommendations)
```

---

## 📁 Repository Structure

The project follows a standard Software Development Life Cycle (SDLC) structure:

```
HDI-Insights/
├── 01_Brainstorming/          # Problem statements, objectives, and research ideation
├── 02_Requirement_Analysis/   # Functional, non-functional, hardware & software stack NFRDs
├── 03_Project_Design/         # System architecture, database layouts, mockups, and diagrams
├── 04_Project_Planning/       # Project schedules, milestones, and week-by-week Gantt charts
├── 05_Project_Development/    # Source directory for the Flask application codebase
│   ├── app.py                 # Core Flask server and endpoint router
│   ├── train_model.py         # ML benchmarking, model training, and serialization
│   ├── requirements.txt       # Core package requirements
│   ├── templates/             # HTML files
│   ├── static/                # CSS themes, Javascript controls, and assets
│   ├── models/                # Serialized model bins (.joblib) and comparison records
│   ├── database/              # SQLite database storage (hdi_history.db)
│   ├── dataset/               # Clean and raw data files
│   └── utils/                 # DB management and PDF creation modules
├── 06_Project_Testing/        # Test cases spreadsheets and test execution summaries
├── 07_Project_Documentation/  # Final reports, manuals, installations, and PPTX slide decks
├── 08_Project_Demonstration/  # Screen demo script, demo.mp4 placeholder, and screenshots
├── LICENSE                    # MIT license
└── README.md                  # Comprehensive root documentation guide
```

---

## 🚀 Setup & Installation

Follow these steps to run the application locally:

### 1. Set Up the Project
```bash
# Navigate to the development folder
cd 05_Project_Development

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Application
```bash
# Launch Flask server
python app.py
```
Open **[http://localhost:5000/](http://localhost:5000/)** in your web browser.

### 3. Model Retraining (Optional)
To retrain the machine learning classifiers and regenerate model comparisons:
```bash
python train_model.py
```

---

## 📊 Model Performance

Our Support Vector Machine (SVM) classifier achieves an overall **98.9% F1-score** on categorical predictions.

| Algorithm | Accuracy | Weighted Precision | Weighted Recall | Weighted F1-Score |
| :--- | :--- | :--- | :--- | :--- |
| **Support Vector Machine (Active)** | **98.9%** | **99.0%** | **98.9%** | **98.9%** |
| Logistic Regression | 98.1% | 98.1% | 98.1% | 98.1% |
| Random Forest | 97.5% | 97.5% | 97.5% | 97.5% |
| K-Nearest Neighbors | 96.2% | 96.2% | 96.2% | 96.2% |
| Decision Tree | 95.6% | 95.7% | 95.6% | 95.6% |

---

## 👤 Developer Profile
* **Developer Name**: Pandu
* **Role**: Machine Learning & Web Applications Software Engineer
* **GitHub**: [https://github.com/pandu0426](https://github.com/pandu0426)
* **Repository**: [https://github.com/pandu0426/HDI-Insights](https://github.com/pandu0426/HDI-Insights)
