import os
from fyers_apiv3 import fyersModel
from dotenv import load_dotenv

load_dotenv()

# Step 1: Session Model setup
session = fyersModel.SessionModel(
    client_id=os.getenv("FYERS_CLIENT_ID"),
    secret_key=os.getenv("FYERS_SECRET_ID"),
    redirect_uri=os.getenv("FYERS_REDIRECT_URL"),
    response_type="code",
    grant_type="authorization_code"
)

# Step 2: Login URL generate karo
print("--- FYERS LOGIN ---")
# Yahan change kiya hai: generate_authcode() bina underscore ke
print(f"Is URL ko browser mein kholein:\n{session.generate_authcode()}")