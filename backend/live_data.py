import os
from fyers_apiv3 import fyersModel
from dotenv import load_dotenv

# .env file se variables load karna
load_dotenv()

client_id = os.getenv("FYERS_CLIENT_ID")
access_token = os.getenv("FYERS_ACCESS_TOKEN")

# Naya FyersModel initialization
fyers = fyersModel.FyersModel(
    client_id=client_id, 
    is_async=False, 
    token=access_token, 
    log_path=""
)

# NIFTY 50 Index ka symbol
symbols = "NSE:NIFTY50-INDEX"

print(f"🔄 Fetching Live Data for {symbols}...\n")

# API ko hit karke Quotes (live price) lana
data = fyers.quotes({"symbols": symbols})

# Data ko clean format mein print karna
if data and "d" in data and len(data["d"]) > 0:
    stock_info = data["d"][0]["v"]
    
    print("✅ LIVE DATA RECEIVED:\n")
    
    # Defensive dictionary parsing using .get()
    print(f"📈 Symbol: {stock_info.get('short_name', symbols)}")
    print(f"💰 Current Price (LTP): ₹{stock_info.get('lp', 'N/A')}")
    print(f"📊 Open: ₹{stock_info.get('open_price', 'N/A')} | High: ₹{stock_info.get('high_price', 'N/A')} | Low: ₹{stock_info.get('low_price', 'N/A')}")
    print(f"📉 Percentage Change: {stock_info.get('chp', 'N/A')}%")
    print(f"🔄 Price Change: ₹{stock_info.get('ch', 'N/A')}")
    
    # Raw data dekhne ke liye (debugging):
    # print("\n🔍 Raw Dictionary:", stock_info)
else:
    print("❌ Error fetching data:", data)