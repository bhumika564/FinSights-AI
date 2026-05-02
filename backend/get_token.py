import os
from fyers_apiv3 import fyersModel
from dotenv import load_dotenv

load_dotenv()

# Paste your complete redirect URL here after login
raw_input = input("👉 Paste your complete redirect URL here after login and press Enter: ").strip()

# Smart Extraction Logic (Defensive Programming)
try:
    if "auth_code=" in raw_input:
        
        auth_code = raw_input.split("auth_code=")[1].split("&")[0]
    else:
        auth_code = raw_input.split("&")[0]
        
    print("🔍 Clean Code Extracted!")
except Exception as e:
    print("❌ URL format is incorrect.")
    exit()

session = fyersModel.SessionModel(
    client_id=os.getenv("FYERS_CLIENT_ID"),
    secret_key=os.getenv("FYERS_SECRET_ID"),
    redirect_uri=os.getenv("FYERS_REDIRECT_URL"),
    response_type="code",
    grant_type="authorization_code"
)

session.set_token(auth_code)
response = session.generate_token()

if response.get("s") == "ok":
    print("\n✅ SUCCESS! Here is your Access Token:\n")
    print(response["access_token"])
    print("\n👉 Copy this token and paste it in your .env file as FYERS_ACCESS_TOKEN=your_token_here")
else:
    print("\n❌ Error:", response)