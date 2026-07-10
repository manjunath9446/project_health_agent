
# 🚦 AI Project Health Intelligence System

An AI-powered multi-agent system that automatically analyzes Microsoft Project schedules, predicts project health, detects execution risks, forecasts schedule delays, and generates executive-ready reports using Large Language Models (LLMs).

---

## 📌 Overview

Managing large enterprise projects often requires manually reviewing hundreds of tasks, milestones, dependencies, and comments before determining the overall project health.

This project automates that process by combining:

- AI-powered project analysis
- Risk Intelligence
- Delay Forecasting
- Executive Summaries
- Weekly Status Reports
- Monthly Executive PowerPoint Presentations

The system transforms Microsoft Project Excel files into actionable business insights for Project Managers and Executives.

---

## ✨ Features

### 📂 Intelligent Project Ingestion

- Upload Microsoft Project (.xlsx) files
- Automatic template detection
- Hierarchy reconstruction
- Data normalization
- Missing data handling
- Data quality validation

---

### 🤖 AI Project Health Assessment

Automatically evaluates:

- Overall Health Score
- Schedule Performance
- Task Progress
- Critical Path
- Milestone Completion
- Resource Allocation

---

### ⚠ Risk Intelligence

Detects

- Delayed Tasks
- Critical Path Risks
- Missing Task Owners
- Dependency Conflicts
- Slow Progress Tasks
- Schedule Bottlenecks

---

### 📈 Forecasting Engine

Predicts

- Expected Delay
- Delay Probability
- Schedule Outlook
- Completion Risk

---

### 💡 AI Recommendations

Generates

- Recovery Plans
- Executive Recommendations
- Priority Actions
- Risk Mitigation Strategies

---

### 📊 Executive Reporting

Automatically creates

- Executive Summary
- Weekly Status Report
- Monthly Portfolio Report
- Executive PowerPoint Presentation

---

## 🏗 System Architecture

```
                Microsoft Project
                      │
                      ▼
              Data Ingestion Layer
                      │
      ┌───────────────┴───────────────┐
      ▼                               ▼
 Data Cleaning                 Data Validation
      │                               │
      └───────────────┬───────────────┘
                      ▼
             Project Normalization
                      │
                      ▼
            Multi-Agent AI Pipeline
                      │
      ┌────────┬────────┬────────┬────────┐
      ▼        ▼        ▼        ▼
 Health     Risk     Forecast   Summary
 Agent      Agent     Agent      Agent
      │
      ▼
 Recommendation Agent
      │
      ▼
 Executive Dashboard
      │
      ├── RAG Status
      ├── Weekly Report
      ├── Monthly PPT
      └── Executive Summary
```

---

## 🧠 AI Pipeline

The system uses multiple specialized AI modules.

- Health Assessment Agent
- Risk Analysis Agent
- Delay Forecast Agent
- Recommendation Agent
- Executive Summary Generator

Each module performs an independent analysis before the final executive dashboard is generated.

---

## 🚦 RAG Methodology

The overall project health is determined using a weighted scoring model.

```
Final Project Score

= 40% × Health Score
+ 25% × (100 − Delay Probability)
+ 20% × (100 − Risk Score)
+ 15% × Data Quality Score
```

| Score | Status |
|--------|--------|
| 80 – 100 | 🟢 Green |
| 60 – 79 | 🟡 Amber |
| Below 60 | 🔴 Red |

The system also generates a plain-English explanation describing why the project received its RAG status.

---

## 📁 Project Structure

```
src/
│
├── agents/
├── api/
├── core/
├── models/
├── schemas/
├── services/
├── utils/
│
streamlit_app/
│
├── pages/
│
├── reports/
│
├── alembic/
│
└── requirements.txt
```

---

## 🛠 Technology Stack

### Backend

- FastAPI
- SQLAlchemy
- SQLite
- Alembic

### Frontend

- Streamlit

### AI

- Groq API
- Llama 3.3 70B
- Multi-Agent Architecture

### Data Processing

- Pandas
- NumPy
- OpenPyXL

### Reporting

- python-pptx
- Matplotlib

---

## 📊 Outputs

For every uploaded project the system generates

- Project Health Score
- RAG Status
- Executive Summary
- Risk Report
- Delay Forecast
- AI Recommendations
- Weekly Report
- Monthly Executive Presentation

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/project-health-agent.git
```

Create virtual environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙ Environment Variables

Create a `.env`

```env
GROQ_API_KEY=your_api_key
GROQ_MODEL=llama-3.3-70b-versatile
DATABASE_URL=sqlite+aiosqlite:///project.db
```

---

## ▶ Running the Backend

```bash
uvicorn src.core.main:app --reload
```

---

## ▶ Running Streamlit

```bash
streamlit run streamlit_app/app.py
```

---



## 🌟 Future Enhancements

- PostgreSQL Support
- Portfolio Dashboard
- Email Scheduler
- Microsoft Project API Integration
- Jira Integration
- Azure DevOps Integration
- Role-Based Authentication
- Predictive Resource Planning

---

## 👨‍💻 Author

**Manjunath R K**

Bachelor of Engineering (Artificial Intelligence & Machine Learning)

---

## 📄 License

This project is developed for educational and research purposes.