import os
from fyers_apiv3 import fyersModel
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

client_id = os.getenv("FYERS_CLIENT_ID")
access_token = os.getenv("FYERS_ACCESS_TOKEN")

# new fyers model initialization with access token
fyers = fyersModel.FyersModel(
    client_id=client_id, 
    is_async=False, 
    token=access_token, 
    log_path=""
)

# NIFTY 50 Index's symbol
symbols = "NSE:NIFTY50-INDEX"

print(f"🔄 Fetching Live Data for {symbols}...\n")

#Hit API to get live quotes(live price and other details) for NIFTY 50
data = fyers.quotes({"symbols": symbols})

# Print the received data in a clean format
if data and "d" in data and len(data["d"]) > 0:
    stock_info = data["d"][0]["v"]
    
    print("✅ LIVE DATA RECEIVED:\n")
    
    
    print(f"📈 Symbol: {stock_info.get('short_name', symbols)}")
    print(f"💰 Current Price (LTP): ₹{stock_info.get('lp', 'N/A')}")
    print(f"📊 Open: ₹{stock_info.get('open_price', 'N/A')} | High: ₹{stock_info.get('high_price', 'N/A')} | Low: ₹{stock_info.get('low_price', 'N/A')}")
    print(f"📉 Percentage Change: {stock_info.get('chp', 'N/A')}%")
    print(f"🔄 Price Change: ₹{stock_info.get('ch', 'N/A')}")
    
    # To see Raw data(debugging):
    # print("\n🔍 Raw Dictionary:", stock_info)
else:
    print("❌ Error fetching data:", data)