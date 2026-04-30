import os
import json
import asyncio
import yfinance as yf
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fyers_apiv3 import fyersModel
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- HELPER FUNCTIONS -----------------

def get_fyers_client():
    return fyersModel.FyersModel(
        client_id=os.getenv("FYERS_CLIENT_ID"),
        token=os.getenv("FYERS_ACCESS_TOKEN"),
        is_async=False, log_path=""
    )

async def fetch_fyers_data(symbols):
    loop = asyncio.get_event_loop()
    fyers = get_fyers_client()
    return await loop.run_in_executor(None, lambda: fyers.quotes({"symbols": ",".join(symbols)}))

async def get_latest_news_async(symbol):
    """Brief report ke liye news fetcher"""
    loop = asyncio.get_event_loop()
    def fetch_news():
        try:
            yf_symbol = "^NSEI" if "NIFTY" in symbol.upper() else f"{symbol.upper()}.NS"
            ticker = yf.Ticker(yf_symbol)
            news = ticker.news
            return " | ".join([n['title'] for n in news[:3]]) if news else "No major recent news."
        except:
            return "News temporarily unavailable."
    return await loop.run_in_executor(None, fetch_news)

# ----------------- API ENDPOINTS -----------------

@app.get("/api/search")
async def search_stock(symbol: str = Query(..., description="Stock symbol to search")):
    try:
        # 1. whaterver user input, convert to uppercase and trim spaces for consistency
        symbol_input = symbol.upper().strip()

        # 2. smart trasnlation for user-friendly inputs
        if symbol_input in ["INFOSYS", "INFY"]:
            target_symbol = "NSE:INFY-EQ"
        elif symbol_input == "ZOMATO":
            target_symbol = "NSE:ZOMATO-EQ"
        elif "NIFTY" in symbol_input:
            target_symbol = "NSE:NIFTY50-INDEX"
        else:
            # standard format for all other stocks
            target_symbol = f"NSE:{symbol_input}-EQ"

        print(f"DEBUG: Backend kya dhundh raha hai -> {target_symbol}")

        movers_symbols = ["NSE:RELIANCE-EQ", "NSE:HDFCBANK-EQ", "NSE:TCS-EQ", "NSE:INFY-EQ", "NSE:ICICIBANK-EQ"]
        all_symbols = [target_symbol] + movers_symbols

        # 3. get data from fyers and news in parallel
        data_task = asyncio.create_task(fetch_fyers_data(all_symbols))
        news_task = asyncio.create_task(get_latest_news_async(symbol_input))
        data, news_headlines = await asyncio.gather(data_task, news_task)

        # 4. search your target stock in fyers data
        searched_item = next((item for item in data.get("d", []) if item.get("n") == target_symbol), None)
        
        # if not found by exact match, try partial match (for user convenience)
        if not searched_item:
            for item in data.get("d", []):
                if symbol_input in item.get("n", ""):
                    searched_item = item
                    break

        # if not found, return 404
        if not searched_item:
            raise HTTPException(status_code=404, detail=f"Stock '{symbol_input}' price not available.")
            
        stock_data = searched_item["v"]

        # 5. to find data of market movers
        movers = []
        for item in data["d"]:
             if item["n"] != target_symbol and item["n"] in movers_symbols:
                v = item["v"]
                movers.append({
                    "symbol": v.get("short_name", item["n"].split(":")[1].split("-")[0]),
                    "price": v.get("lp"),
                    "change": v.get("chp")
                })

        # 6. Groq AI Analysis
        try:
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            prompt = f"""Analyze {symbol_input} stock. 
            Price: ₹{stock_data.get('lp')}, Change: {stock_data.get('chp')}%. 
            News: {news_headlines}
            
            Instruction: Be decisive based on price change and news. 
            If change > 1.5% and news is positive, suggest 'Invest'. 
            If change < -1.5% or news is negative, suggest 'Avoid'. 
            Otherwise, 'Hold'.
            
            Return ONLY JSON:
            {{"sentiment": "2-sentence report", "confidence": "XX%", "investment_advice": "Invest/Hold/Avoid + short reason"}}"""
            
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
                temperature=0.5, 
                response_format={"type": "json_object"}
            )
            ai_data = json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"AI Error: {e}") 
            ai_data = {"sentiment": "Trend is stable.", "confidence": "80%", "investment_advice": "Hold for now."}

        # 7. Final data to frontend 
        return {
            "main_stock": {
                "name": symbol_input,
                "price": stock_data.get("lp"),
                "change": stock_data.get("chp"),
                "high": stock_data.get("high_price"),
                "low": stock_data.get("low_price"),
                "open": stock_data.get("open_price"),
                "analysis": ai_data.get("sentiment"),
                "accuracy": ai_data.get("confidence"),
                "investment_advice": ai_data.get("investment_advice")
            },
            "movers": movers
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Search failed")


@app.get("/api/market-analysis")
async def get_market_analysis():
    try:
        symbols = ["NSE:NIFTY50-INDEX", "NSE:RELIANCE-EQ", "NSE:HDFCBANK-EQ", "NSE:TCS-EQ", "NSE:INFY-EQ", "NSE:ICICIBANK-EQ"]
        
        data_task = asyncio.create_task(fetch_fyers_data(symbols))
        news_task = asyncio.create_task(get_latest_news_async("NIFTY 50"))
        
        data, news_headlines = await asyncio.gather(data_task, news_task)

        if not data or "d" not in data:
            raise HTTPException(status_code=401, detail="Invalid Data.")

        nifty_item = next((item for item in data["d"] if item["n"] == "NSE:NIFTY50-INDEX"), None)
        nifty = nifty_item["v"]
        
        movers = []
        for item in data["d"]:
            if "NIFTY50" not in item["n"]:
                v = item["v"]
                movers.append({
                    "symbol": v.get("short_name", item["n"].split(":")[1].split("-")[0]),
                    "price": v.get("lp"),
                    "change": v.get("chp")
                })

        try:
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            prompt = f"Analyze Nifty 50 at ₹{nifty.get('lp')}. News: {news_headlines}. Return JSON: sentiment, confidence, investment_advice."
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            ai_data = json.loads(response.choices[0].message.content)
        except:
            ai_data = {"sentiment": "Market is steady.", "confidence": "85%", "investment_advice": "Hold."}

        return {
            "main_stock": {
                "name": "NIFTY 50 INDEX",
                "price": nifty.get("lp"),
                "change": nifty.get("chp"),
                "high": nifty.get("high_price"),
                "low": nifty.get("low_price"),
                
                "open": nifty.get("open_price"), 
                "analysis": ai_data.get("sentiment"),
                "accuracy": ai_data.get("confidence"),
                "investment_advice": ai_data.get("investment_advice")
            },
            "movers": movers
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server Error")