import os
import pyotp
from dotenv import load_dotenv

load_dotenv()

# take TOTP secret from .env file
totp_secret = os.getenv("FYERS_TOTP_SECRET")

if not totp_secret:
    print("❌ Error: FYERS_TOTP_SECRET is not found.")
else:
    # Generate TOTP 
    totp = pyotp.TOTP(totp_secret)
    current_otp = totp.now()
    print("✅ Your 6-Digit TOTP is:", current_otp)