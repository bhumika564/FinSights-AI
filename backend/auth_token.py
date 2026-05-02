"""
FinSights - Daily Token Generator
Run Daily - every morning: python auth_token.py
"""
import os
import webbrowser
from flask import Flask, request
from fyers_apiv3 import fyersModel
from dotenv import load_dotenv, set_key

load_dotenv()

CLIENT_ID = os.getenv("FYERS_CLIENT_ID")
SECRET_KEY = os.getenv("FYERS_SECRET_ID")
REDIRECT_URI = "http://127.0.0.1:5000/callback"
ENV_FILE = os.path.join(os.path.dirname(__file__), ".env")

# ==========================================
# Step 1: Create Auth URL and Open Browser
# ==========================================
session = fyersModel.SessionModel(
    client_id=CLIENT_ID,
    secret_key=SECRET_KEY,
    redirect_uri=REDIRECT_URI,
    response_type="code",
    grant_type="authorization_code"
)

auth_url = session.generate_authcode()
print("\n" + "="*50)
print("  FinSights - Daily Token Refresh")
print("="*50)
print("\n✅ Fyers login page is opening...")
print("   Login → Allow → Done!\n")
webbrowser.open(auth_url)

# ==========================================
# Step 2: Callback, auth_code capture, token generation, .env update
# ==========================================
auth_app = Flask(__name__)

@auth_app.route("/callback")
def callback():
    auth_code = request.args.get("auth_code")
    if not auth_code:
        return "<h2>❌ Auth code not found. Try again.</h2>", 400

    # Step 3: Create session with auth code and generate token
    session.set_token(auth_code)
    token_res = session.generate_token()

    if token_res.get("s") != "ok":
        return f"<h2>❌ Token error: {token_res}</h2>", 400

    access_token = token_res["access_token"]

    # Step 4: Save automatically to .env file
    set_key(ENV_FILE, "FYERS_ACCESS_TOKEN", access_token)

    print("\n" + "="*50)
    print("  ✅ TOKEN SUCCESSFULLY UPDATED!")
    print("="*50)
    print("\n  Close this terminal.\n")
    print("    Run 'python main.py' to start the engine with the new token.\n")

    # Server band karo
    shutdown = request.environ.get("werkzeug.server.shutdown")
    if shutdown:
        shutdown()

    return """
    <html><body style="font-family:Arial; text-align:center; padding:50px; background:#020817; color:white;">
        <h1 style="color:#22c55e;">✅ Token Updated Successfully!</h1>
        <p style="color:#94a3b8;">Close this terminal and run 'python main.py' to start the engine with the new token.</p>
    </body></html>
    """

if __name__ == "__main__":
    # Port 5000 pe callback(only for auth)
    auth_app.run(port=5000, debug=False)