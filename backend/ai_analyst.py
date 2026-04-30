import os
from fyers_apiv3 import fyersModel
from groq import Groq
from dotenv import load_dotenv

# Variables load karna
load_dotenv()

# 1. Fyers API Setup
fyers = fyersModel.FyersModel(
    client_id=os.getenv("FYERS_CLIENT_ID"),
    is_async=False,
    token=os.getenv("FYERS_ACCESS_TOKEN"),
    log_path=""
)

# 2. Live Data Fetch Karna
symbols = "NSE:NIFTY50-INDEX"
print("🔄 Fetching Live Market Data from Fyers...\n")
data = fyers.quotes({"symbols": symbols})

if data and "d" in data and len(data["d"]) > 0:
    stock_info = data["d"][0]["v"]
    price = stock_info.get('lp', 'N/A')
    chg = stock_info.get('chp', 'N/A')
    high = stock_info.get('high_price', 'N/A')
    low = stock_info.get('low_price', 'N/A')
    
    print(f"✅ Data Received: NIFTY 50 is trading at ₹{price} ({chg}%)\n")
    
    # 3. Groq AI Integration
    print("🧠 Sending data to Groq AI for instant analysis...\n")
    
    # Groq Client setup
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    # AI ke liye Prompt design karna
    prompt = f"""
    You are an expert AI Stock Market Analyst working for Ethara AI.
    Here is the live data for NIFTY 50 index in the Indian Stock Market:
    - Current Price: ₹{price}
    - Percentage Change: {chg}%
    - Today's High: ₹{high}
    - Today's Low: ₹{low}

    Give a short, crisp 3-4 sentence analysis of the current market sentiment based on this data. 
    Tell the user if it's bearish, bullish, or neutral, and what the high/low numbers indicate. 
    Keep the tone professional, analytical, and easy to understand.
    """
    
    # 🚨 YAHAN MODEL UPDATE KIYA HAI 🚨
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile", 
        temperature=0.5
    )
    
    print("📊 AI ANALYST REPORT:")
    print("=" * 50)
    print(response.choices[0].message.content)
    print("=" * 50)

else:
    print("❌ Error fetching data:", data)