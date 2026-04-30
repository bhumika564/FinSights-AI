import os
from fyers_apiv3 import fyersModel
from dotenv import load_dotenv

load_dotenv()

# Ab aap browser se POORI URL copy karke yahan paste kar sakti hain!
raw_input = input("👉 Browser se poori Redirect URL yahan paste karein aur Enter dabayein: ").strip()

# Smart Extraction Logic (Defensive Programming)
try:
    if "auth_code=" in raw_input:
        # URL mein se auth_code nikalna aur &state ko hatana
        auth_code = raw_input.split("auth_code=")[1].split("&")[0]
    else:
        auth_code = raw_input.split("&")[0]
        
    print("🔍 Clean Code Extracted!")
except Exception as e:
    print("❌ URL sahi format mein nahi hai.")
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
    print("\n✅ SUCCESS! Yeh raha aapka Access Token:\n")
    print(response["access_token"])
    print("\n👉 Is lambe token ko copy karein aur apni .env file mein FYERS_ACCESS_TOKEN= ke aage paste kar dein.")
else:
    print("\n❌ Error:", response)