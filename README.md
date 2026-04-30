# 📈 FinSights-AI: Real-Time Stock Analysis Dashboard

**FinSights-AI** is a professional full-stack financial dashboard that provides real-time NSE stock data paired with AI-driven market sentiment analysis. Built for modern traders, it uses Large Language Models (LLMs) to provide actionable insights.

## ❓ How to Use

Follow these steps to get real-time insights for any company:

- **Search for a Company**: Enter the name of any listed company (e.g., **Swiggy**, **Zomato**, or **Reliance**) in the search bar.
- **Real-time Share Price**: Get the current market price instantly.
- **Interactive Charts**: View **Intraday Graphs** and **Stock Charts** to track performance and price movements.
- **AI Recommendations**: Our AI agent analyzes market trends to give you clear signals:
  - **Invest/Buy**: Long-term growth is expected.
  - **Hold**: The market is stable.
  - **Sell/Avoid**: Risks have been identified.
- **Financial Analysis**: Get a detailed AI-generated summary explaining the recommendation based on news and technical indicators.


## 🌐 Go to Website
Click here to access the live application: **[FinSights-AI Live](https://fin-sights-ai.vercel.app/)**


## 🚀 Project Deployment Links
- **Frontend URL:** [https://fin-sights-ai.vercel.app/](https://fin-sights-ai.vercel.app/)
- **Backend API:** [https://finsights-ai-2zsd.onrender.com](https://finsights-ai-2zsd.onrender.com)


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
