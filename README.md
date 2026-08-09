# Industrial AI Predictive Maintenance System

An end-to-end predictive maintenance platform that combines **machine learning, physics-based feature engineering, retrieval-augmented generation (RAG), and generative AI** to predict industrial machine failure risk and provide contextual maintenance explanations.

The system exposes a **FastAPI backend**, stores prediction history in **PostgreSQL**, and provides an interactive **Streamlit dashboard**. The backend is deployed on **Render**.

---

## 🚀 Overview

Industrial machines can develop faults due to changing operating conditions such as torque, rotational speed, temperature, and tool wear.

This project builds a complete predictive-maintenance pipeline:

```text
Machine Operating Data
        │
        ▼
Physics-Based Feature Engineering
        │
        ▼
Machine Learning Model
        │
        ├── Prediction
        ├── Failure Probability
        └── Risk Level
                │
                ▼
        Maintenance Knowledge Retrieval
                │
                ▼
          Gemini AI Explanation
                │
                ▼
        PostgreSQL Prediction History
                │
                ▼
          Streamlit Dashboard
```

---

## ✨ Key Features

### 🤖 Machine Learning Prediction

The system predicts whether a machine is likely to experience failure based on operating conditions including:

* Air temperature
* Process temperature
* Rotational speed
* Torque
* Tool wear
* Machine type

The model returns:

* Failure prediction
* Failure probability
* Risk level

---

### ⚙️ Physics-Based Features

In addition to raw machine measurements, the system derives additional features representing machine operating behavior, including:

* Power
* Temperature difference
* Wear progression

These features provide additional information about the physical operating state of the machine.

---

### 📚 Maintenance Knowledge Retrieval

The system maintains a PostgreSQL-based collection of maintenance knowledge.

For each prediction, relevant maintenance information is retrieved based on the predicted condition and machine operating parameters.

The retrieved information is then supplied to the generative AI layer as context.

---

### 🧠 AI Maintenance Explanations

The system uses Google's Gemini API to generate a practical explanation for each prediction.

The explanation covers:

1. Why the machine is considered to be at that risk level
2. Which operating parameters should be investigated
3. Recommended maintenance actions

The AI is explicitly instructed to:

* Treat predictions as risk indicators rather than guarantees
* Avoid inventing manufacturer limits
* Avoid unsupported numerical operating limits
* Base recommendations on retrieved maintenance knowledge
* Keep recommendations practical and concise

---

### 🗄️ PostgreSQL Prediction History

Every prediction is stored in PostgreSQL along with:

* Timestamp
* Machine type
* Machine operating parameters
* Physics-derived features
* Prediction
* Failure probability
* Risk level
* AI maintenance explanation

This allows predictions to be reviewed after they are generated.

---

### 📊 Interactive Streamlit Dashboard

The Streamlit frontend provides:

* Machine input controls
* Prediction results
* Failure probability
* Risk classification
* Prediction history
* Filtering by machine type
* Filtering by risk level
* Filtering by prediction
* Expandable AI maintenance analysis
* CSV export
* Analytics dashboard

---

### 🛡️ AI Failure Handling

The prediction system does not depend on Gemini being continuously available.

If the AI service is unavailable or its API quota is exceeded, the machine-learning prediction is still saved and returned with a fallback message.

```text
ML Prediction
     │
     ▼
Gemini Available? ─── Yes ──► AI Explanation
     │
     No
     │
     ▼
Fallback Explanation
     │
     ▼
Prediction Still Saved
```

This prevents an external generative-AI service failure from taking down the core prediction system.

---

## 🏗️ System Architecture

```text
                     ┌──────────────────────┐
                     │  Streamlit Frontend  │
                     └──────────┬───────────┘
                                │
                                │ HTTP
                                ▼
                     ┌──────────────────────┐
                     │    FastAPI Backend   │
                     └──────────┬───────────┘
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
              ▼                 ▼                 ▼
      ┌──────────────┐  ┌───────────────┐  ┌──────────────┐
      │ ML Predictor │  │ Knowledge RAG │  │  PostgreSQL  │
      └──────┬───────┘  └───────┬───────┘  └──────────────┘
             │                  │
             └──────────┬───────┘
                        ▼
                ┌───────────────┐
                │ Gemini API    │
                │ AI Explanation│
                └───────────────┘
```

---

## 🛠️ Technology Stack

| Component           | Technology                 |
| ------------------- | -------------------------- |
| Programming         | Python                     |
| Machine Learning    | Scikit-learn               |
| Backend API         | FastAPI                    |
| Database            | PostgreSQL                 |
| Frontend            | Streamlit                  |
| Generative AI       | Google Gemini API          |
| Knowledge Retrieval | PostgreSQL-based retrieval |
| Data Processing     | Pandas                     |
| Deployment          | Render                     |
| Version Control     | Git / GitHub               |

---

## 📁 Project Structure

```text
predictive-maintenance-project/
│
├── app/
│   ├── main.py
│   ├── crud.py
│   ├── database.py
│   ├── llm.py
│   ├── logger.py
│   ├── models.py
│   ├── physics.py
│   ├── predictor.py
│   ├── rag.py
│   └── schemas.py
│
├── data/
│
├── knowledge/
│
├── models/
│
├── notebooks/
│
├── streamlit/
│   └── app.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🔄 Prediction Workflow

When a user submits machine operating conditions:

### 1. Input

The Streamlit application sends machine parameters to the FastAPI backend.

### 2. Feature Engineering

The backend calculates physics-derived features such as power, temperature difference, and wear progression.

### 3. Machine Learning Prediction

The trained machine-learning model generates:

```text
Prediction
Failure Probability
Risk Level
```

### 4. Knowledge Retrieval

Relevant maintenance information is retrieved from the knowledge database.

### 5. AI Explanation

The retrieved knowledge and machine conditions are passed to Gemini to generate a contextual maintenance explanation.

### 6. Persistence

The complete prediction and AI explanation are stored in PostgreSQL.

### 7. Visualization

The Streamlit application displays the result and adds it to prediction history.

---

## 🌐 Deployment

The FastAPI backend is deployed on Render.

The application can be accessed through the deployed API and Streamlit frontend.

FastAPI automatically provides interactive API documentation through:

```text
/docs
```

---

## 🔐 Environment Variables

Create a `.env` file for local development:

```env
DATABASE_URL=your_postgresql_connection_string
GEMINI_API_KEY=your_gemini_api_key
API_URL=your_fastapi_api_url
```

**Never commit `.env` or API keys to GitHub.**

---

## 💻 Local Setup

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd predictive-maintenance-project
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create `.env`:

```env
DATABASE_URL=your_postgresql_connection_string
GEMINI_API_KEY=your_gemini_api_key
API_URL=http://localhost:8000
```

### 5. Start FastAPI

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

### 6. Start Streamlit

In another terminal:

```bash
streamlit run streamlit/app.py
```

---

## 📌 Example API Request

### `POST /predict`

```json
{
    "air_temp": 300,
    "process_temp": 310,
    "rotational_speed": 1500,
    "torque": 40,
    "tool_wear": 100,
    "machine_type": "M"
}
```

The API returns the machine prediction, probability, risk level, recommended actions, and AI-generated maintenance explanation when the Gemini service is available.

---

## 🔮 Future Improvements

Potential improvements include:

* More advanced semantic/vector-based knowledge retrieval
* Automated model retraining
* Real-time machine sensor integration
* Model monitoring and drift detection
* Explainable ML techniques such as SHAP
* Authentication and role-based access
* Automated maintenance scheduling
* Historical trend-based failure forecasting
* More robust AI evaluation and hallucination monitoring

---

## 🎯 Project Goal

The goal of this project is to demonstrate how **machine learning, engineering-domain knowledge, backend APIs, databases, retrieval systems, and generative AI** can be combined into a practical industrial AI application.

Rather than only producing a binary failure prediction, the system attempts to provide an end-to-end workflow from **machine data → risk prediction → contextual explanation → maintenance decision support**.
