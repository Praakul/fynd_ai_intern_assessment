# AI Intern Assessment

This repository contains the solution for the AI Engineering Internship Take-Home Assessment. It includes an AI-powered sentiment analysis experiment and a full-stack feedback collection dashboard.

## 📂 Project Structure
```bash
├── task_one/
│   ├── task_one.ipynb      # Task 1: Sentiment Analysis Notebook (Zero-shot, Few-shot, CoT)
│   └── yelp.csv            # Dataset (Sampled)
├── task_two/
│   ├── app.py              # Task 2: Frontend (Streamlit User & Admin Dashboards)
│   ├── utils.py            # Task 2: Backend (AI Logic & Data Handling)
│   └── feedback_data.csv   # Local database for the web app
├── requirements.txt        # Dependencies
└── README.md               # Documentation
```

## 🚀 Quick Start

### 1. Setup

Clone the repository and install dependencies:
```bash
git clone github.com/Praakul/fynd_ai_intern_assessment.git
cd fynd_ai_intern_assessment
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the root directory and add your Gemini API Key:
```
GOOGLE_API_KEY="AIzaSy...YourKeyHere"
```

**Note:** Both tasks have a "Mock Mode" fallback enabled by default. If the API key is missing or quota is exceeded (429 Error), the system automatically switches to simulated data to ensure the code runs smoothly for review.

## 🟢 Task 1: Rating Prediction via Prompting

**Goal:** Classify Yelp reviews (1-5 stars) using Gemini 1.5 Flash.

**Strategies Tested:**
- **Zero-Shot:** Direct classification.
- **Few-Shot:** Providing 3 labeled examples (Positive, Neutral, Negative).
- **Chain-of-Thought (CoT):** Forcing step-by-step reasoning (Pros vs Cons).

**Optimization:** Implemented Batch Processing and Exponential Backoff to handle API rate limits.

**How to Run:** Open `task_one/task_one.ipynb` in Jupyter Notebook or VS Code and run all cells.

## 🔵 Task 2: Two-Dashboard AI Feedback System

**Goal:** A web application for Users to submit feedback and Admins to view AI-generated insights.

**Architecture:** Modular design separating Frontend (`app.py`) from Backend Logic (`utils.py`).

**Features:**
- **User Dashboard:** Accepts ratings/reviews and provides an instant AI-generated reply.
- **Admin Dashboard:** Displays live analytics, AI summaries, and recommended action items.
- **One-Shot Analysis:** Uses a single optimized prompt to generate the Reply, Summary, and Action simultaneously for efficiency.

**Live Deployment:**
- User Dashboard: [Link to your Streamlit App]
- Admin Dashboard: [Link to your Streamlit App] (Use the Sidebar to toggle views)

**How to Run Locally:**
```bash
streamlit run task_two/app.py
```

## 🛡️ Robustness Features

- **Rate Limit Handling:** Both tasks include logic to handle 429 Resource Exhausted errors gracefully.
- **Mock Data Fallback:** If the API is unavailable during grading, the system generates synthetic responses so the UI and Logic can still be evaluated.