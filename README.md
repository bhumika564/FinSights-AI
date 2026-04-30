# 📈 FinSights-AI: Real-Time Stock Analysis Dashboard

**FinSights-AI** is a professional full-stack financial dashboard that provides real-time NSE stock data paired with AI-driven market sentiment analysis. Built for modern traders, it uses Large Language Models (LLMs) to provide actionable insights.

## 🚀 Key Features

- **Real-Time Data Fetching:** Live price action, High/Low, and Open data using **Fyers API**.
- **AI Sentiment Engine:** Uses **Groq (Llama 3.1)** to analyze trends and provide "Invest," "Hold," or "Avoid" suggestions.
- **Concurrent Execution:** Run both FastAPI backend and Next.js frontend with a single command.
- **Clean UI:** Modern, dark-themed dashboard built with Tailwind CSS.

## 🛠️ Tech Stack

- **Frontend:** Next.js 15, Tailwind CSS, Lucide Icons.
- **Backend:** FastAPI (Python), Uvicorn.
- **AI:** Llama-3.1-8b (Groq API).
- **Market Data:** Fyers Open API v3.

## 📦 Project Structure

```text
FinSights-AI/
├── frontend/        # Next.js Application
├── backend/         # FastAPI Server & AI Logic
├── package.json     # Root config for concurrent execution
└── .gitignore       # Credential security
```

## ⚙️ Setup & Installation

**Clone the repository:**

```bash
git clone https://github.com/bhumika564/FinSights-AI.git
```

**Install Dependencies:**

```bash
npm install
```

**Run the Dashboard:**

```bash
npm run dev
```

## 🔧 Save aur Push Karein

Ab ise GitHub par bhejne ke liye terminal mein ye 3 commands chalayein:

```bash
# 1. Changes add karein
git add README.md

# 2. Commit karein
git commit -m "Added professional README documentation"

# 3. GitHub par push karein
git push origin main
```