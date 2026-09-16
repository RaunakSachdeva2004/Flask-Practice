# 🧪 Flask Practice & MLOps Model Serving

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask 3.x](https://img.shields.io/badge/flask-3.x-green.svg)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.4+-orange.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A hands-on, professionally structured repository for mastering web development, REST APIs, and Machine Learning model serving with **Flask**, created as part of the **MLOps Bootcamp** curriculum.

---

## 📌 Overview

This repository demonstrates the step-by-step evolution of Flask applications from minimal routing to production-grade ML inference endpoints:
1. **Core Routing & WSGI Basics:** Application setup, dynamic routing, and HTTP methods.
2. **Dynamic UI with Jinja2:** Template inheritance, loops, conditionals, and asset management.
3. **RESTful API Design:** Standard HTTP verbs (`GET`, `POST`, `PUT`, `DELETE`), status codes, and JSON serialization.
4. **Error Handling & Resilience:** Granular HTTP exceptions, `abort()`, and centralized `@app.errorhandler`.
5. **MLOps Model Serving:** End-to-end pipeline training, model serialization, health checks, and single/batch inference APIs.

---

## 📂 Repository Structure

```text
Flask-Practice/
├── 01_basics/                     # Fundamental Flask concepts
│   ├── app.py                    # Minimal WSGI application & routing
│   ├── main.py                   # HTML template rendering
│   └── getpost.py                # GET/POST methods & form handling
├── 02_templates_jinja/            # Jinja2 templating engine & dynamic URLs
│   └── jinja.py                  # Expressions, loops, variable rules, and forms
├── 03_rest_api/                   # RESTful API development
│   ├── api.py                    # In-memory CRUD JSON API
│   └── data/
│       └── sample.json           # Sample JSON payloads for testing
├── 04_error_handling/             # Robust error handling & HTTP status codes
│   └── error_handling.py         # abort(), custom error handlers (400, 403, 404, 500)
├── 05_ml_pipeline/                # MLOps ML inference pipeline
│   ├── train_model.py            # Model training & artifact serialization
│   ├── ml_inference.py           # Production-ready Flask inference server
│   └── models/
│       └── model.joblib          # Serialized scikit-learn model artifact
├── static/                        # Shared static assets
│   ├── css/
│   │   └── style.css             # Global stylesheet
│   └── script/
│       └── script.js             # Client-side scripts
├── templates/                     # Jinja2 HTML templates
│   ├── about.html
│   ├── form.html
│   ├── getresult.html
│   ├── home.html
│   ├── index.html
│   ├── result.html
│   └── result1.html
├── .gitignore                     # Git ignore rules
├── requirements.txt               # Pinned project dependencies
└── README.md                      # Project documentation
```

---

## ⚙️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/RaunakSachdeva2004/Flask-Practice.git
cd Flask-Practice
```

### 2. Create and Activate a Virtual Environment

```bash
# Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1

# Windows (Command Prompt)
python -m venv venv
venv\Scripts\activate.bat

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Modules

Each module is self-contained and can be executed directly from the root directory:

### Module 1: Flask Basics & Routing
```bash
# Minimal WSGI App
python 01_basics/app.py

# Template Rendering
python 01_basics/main.py

# GET & POST Form Handling
python 01_basics/getpost.py
```
Visit: `http://127.0.0.1:5000/`

### Module 2: Jinja2 Templates & Dynamic URLs
```bash
python 02_templates_jinja/jinja.py
```
- Variable rule route: `http://127.0.0.1:5000/success/85`
- Dynamic dictionary iteration: `http://127.0.0.1:5000/successres/78`
- Grade calculator form: `http://127.0.0.1:5000/calculate`

### Module 3: RESTful API
```bash
python 03_rest_api/api.py
```
- Retrieve all items:
  ```bash
  curl -X GET http://127.0.0.1:5000/items
  ```
- Create a new item:
  ```bash
  curl -X POST http://127.0.0.1:5000/items -H "Content-Type: application/json" -d "{\"name\": \"MLOps Pipeline\", \"description\": \"Setup DVC and MLflow\"}"
  ```

### Module 4: Error Handling & Custom Status Codes
```bash
python 04_error_handling/error_handling.py
```
- Trigger custom 404 handler: `curl -X GET http://127.0.0.1:5000/books/999`
- Trigger custom 403 abort: `curl -X GET http://127.0.0.1:5000/trigger-403`
- Trigger division error handling: `curl -X GET "http://127.0.0.1:5000/divide?a=10&b=0"`

### Module 5: ML Inference Pipeline
```bash
# 1. Train and serialize the model (creates 05_ml_pipeline/models/model.joblib)
python 05_ml_pipeline/train_model.py

# 2. Launch the ML Inference Server
python 05_ml_pipeline/ml_inference.py
```

#### Test Endpoints:
- **Health Check:**
  ```bash
  curl -X GET http://127.0.0.1:5000/health
  ```
- **Model Metadata:**
  ```bash
  curl -X GET http://127.0.0.1:5000/metadata
  ```
- **Single Instance Prediction:**
  ```bash
  curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d "{\"features\": [5.1, 3.5, 1.4, 0.2]}"
  ```
- **Batch Prediction:**
  ```bash
  curl -X POST http://127.0.0.1:5000/predict_batch -H "Content-Type: application/json" -d "{\"instances\": [[5.1, 3.5, 1.4, 0.2], [6.7, 3.0, 5.2, 2.3]]}"
  ```

---

## 🛠️ Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **[Python](https://www.python.org/)** | Core programming language |
| **[Flask](https://flask.palletsprojects.com/)** | Lightweight WSGI web framework & REST API engine |
| **[Jinja2](https://palletsprojects.com/p/jinja/)** | Fast, expressive HTML templating engine |
| **[Scikit-Learn](https://scikit-learn.org/)** | Machine Learning model training & preprocessing pipeline |
| **[Joblib](https://joblib.readthedocs.io/)** | Lightweight model serialization & artifact persistence |
| **[NumPy](https://numpy.org/)** | Efficient numerical array manipulation for model inputs |

---

## 👤 Author

- **Raunak Sachdeva** - [@RaunakSachdeva2004](https://github.com/RaunakSachdeva2004)