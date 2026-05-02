import os
import logging
import pandas as pd
import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS
from fyers_apiv3 import fyersModel
from groq import Groq
from datetime import datetime, timedelta
from dotenv import load_dotenv

# ==========================================
# 1. CONFIGURATION & LOGGING
# ==========================================
load_dotenv()
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename="finsights_pro.log"
)

app = Flask(__name__)
CORS(app)

# ==========================================
# 2. CORE TRADING ENGINE CLASS
# ==========================================
class FinSightsEngine:
    def __init__(self):
        self.client_id = os.getenv("FYERS_CLIENT_ID")
        self.access_token = os.getenv("FYERS_ACCESS_TOKEN")
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.fyers = None
        self.groq = None
        self.connect()

    def connect(self):
        try:
            self.fyers = fyersModel.FyersModel(
                client_id=self.client_id, 
                token=self.access_token, 
                is_async=False, 
                log_path=""
            )
            self.groq = Groq(api_key=self.groq_key)
            logging.info("Successfully connected to Fyers and Groq.")
        except Exception as e:
            logging.error(f"Connection Error: {e}")

    def get_live_quotes(self, symbols):
        try:
            res = self.fyers.quotes({"symbols": ",".join(symbols)})
            return res['d'] if res.get('s') == 'ok' else []
        except Exception as e:
            return []

    def get_historical_data(self, symbol, days=60):
        try:
            end = datetime.now().strftime('%Y-%m-%d')
            start = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            data = {
                "symbol": symbol, "resolution": "D", "date_format": "1",
                "range_from": start, "range_to": end, "cont_flag": "1"
            }
            res = self.fyers.history(data)
            if res.get('s') == 'ok':
                return pd.DataFrame(res['candles'], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            return pd.DataFrame()
        except Exception as e:
            logging.error(f"History Fetch Error: {e}")
            return pd.DataFrame()

    def calculate_indicators(self, df):
        if df.empty: return {}
        df['sma_20'] = df['close'].rolling(window=20).mean()
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        last_row = df.iloc[-1]
        return {
            "sma_20": round(last_row['sma_20'], 2),
            "rsi": round(last_row['rsi'], 2),
            "trend": "Bullish" if last_row['close'] > last_row['sma_20'] else "Bearish"
        }

    def generate_ai_report(self, symbol_name, price, indicators, change):
        try:
            prompt = (
                f"You are a professional Indian stock market analyst. Analyze {symbol_name} which is at Rs.{price}. "
                f"RSI is {indicators.get('rsi', 'N/A')}, Trend is {indicators.get('trend', 'N/A')}, "
                f"today's change is {change}%. "
                f"Give a concise 2-3 sentence market outlook. "
                f"Then list exactly 3 Key Drivers and 3 What to Watch points. "
                f"Format as JSON with keys: outlook (string), sentiment (Bullish/Bearish/Neutral), "
                f"accuracy (realistic percentage e.g. 78%), "
                f"key_drivers (list of 3 strings), what_to_watch (list of 3 strings). "
                f"Return ONLY valid JSON, no extra text."
            )
            res = self.groq.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
            )
            import json
            content = res.choices[0].message.content.strip()
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            return json.loads(content.strip())
        except Exception as e:
            logging.error(f"AI Report Error: {e}")
            return {
                "outlook": "Market analysis temporarily unavailable.",
                "sentiment": "Neutral",
                "accuracy": "N/A",
                "key_drivers": ["Global market trends", "FII/DII activity", "Sectoral momentum"],
                "what_to_watch": ["Key resistance levels", "Support zones", "Upcoming economic data"]
            }

    def get_market_movers(self):
        symbols = [
            "NSE:RELIANCE-EQ", "NSE:HDFCBANK-EQ", "NSE:TCS-EQ", 
            "NSE:INFY-EQ", "NSE:ICICIBANK-EQ"
        ]
        try:
            res = self.fyers.quotes({"symbols": ",".join(symbols)})
            movers = []
            if res.get('s') == 'ok':
                for item in res['d']:
                    v = item['v']
                    movers.append({
                        "symbol": v.get('short_name', item['n'].split(':')[1].replace('-EQ','')),
                        "price": round(v.get('lp', 0), 2),
                        "change": round(v.get('chp', 0), 2)
                    })
            return movers
        except Exception as e:
            logging.error(f"Movers Error: {e}")
            return []


engine = FinSightsEngine()

# ==========================================
# 3. HELPER FUNCTION
# ==========================================
def build_stock_response(fyers_symbol, display_name):
    quotes = engine.get_live_quotes([fyers_symbol])
    if not quotes:
        return None
    
    v = quotes[0]['v']
    price = v.get('lp', 0)
    change = round(v.get('chp', 0), 2)
    
    df = engine.get_historical_data(fyers_symbol, days=60)
    indicators = engine.calculate_indicators(df)
    ai = engine.generate_ai_report(display_name, price, indicators, change)
    movers = engine.get_market_movers()

    return {
        "main_stock": {
            "name": display_name,
            "price": round(price, 2),
            "change": change,
            "open": round(v.get('open_price', 0), 2),
            "high": round(v.get('high_price', 0), 2),
            "low": round(v.get('low_price', 0), 2),
            "analysis": ai.get("outlook"),
            "sentiment": ai.get("sentiment"),
            "accuracy": ai.get("accuracy"),
            "key_drivers": ai.get("key_drivers"),
            "what_to_watch": ai.get("what_to_watch"),
            "technical": indicators,
            "investment_advice": f"{'Consider buying on dips' if ai.get('sentiment') == 'Bullish' else 'Stay cautious, wait for reversal' if ai.get('sentiment') == 'Bearish' else 'Hold positions, market is consolidating'}",
        },
        "movers": movers,
        "chart_data": df.tail(15).to_dict(orient='records') if not df.empty else []
    }

# ==========================================
# 4. API ROUTES
# ==========================================

@app.route('/api/market-analysis', methods=['GET'])
def market_analysis():
    """Default - NIFTY 50"""
    result = build_stock_response("NSE:NIFTY50-INDEX", "NIFTY 50 INDEX")
    if not result:
        return jsonify({"error": "Fyers token expired"}), 401
    return jsonify(result)


@app.route('/api/search', methods=['GET'])
def search_stock():
    """Koi bhi stock search karo - e.g. ?symbol=RELIANCE"""
    symbol = request.args.get('symbol', '').upper().strip()
    if not symbol:
        return jsonify({"error": "Symbol required"}), 400
    
    fyers_symbol = f"NSE:{symbol}-EQ"
    result = build_stock_response(fyers_symbol, symbol)
    if not result:
        return jsonify({"error": f"Could not fetch data for {symbol}"}), 404
    return jsonify(result)


@app.route('/api/v1/user/profile', methods=['GET'])
def get_fyers_profile():
    try:
        profile = engine.fyers.get_profile()
        return jsonify(profile)
    except:
        return jsonify({"status": "error", "message": "Could not fetch profile"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)