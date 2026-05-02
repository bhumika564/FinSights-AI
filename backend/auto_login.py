import os
import pyotp
import webbrowser
from urllib.parse import urlparse, parse_qs
from fyers_apiv3 import fyersModel
from dotenv import load_dotenv

# Load .env file
load_dotenv()

FYERS_CLIENT_ID = os.getenv("FYERS_CLIENT_ID")
FYERS_SECRET_ID = os.getenv("FYERS_SECRET_ID") 
FYERS_REDIRECT_URL = os.getenv("FYERS_REDIRECT_URL")
FYERS_TOTP_SECRET = os.getenv("FYERS_TOTP_SECRET")

def manual_login_flow():
    print("🚀 Fyers API Login Process Start...\n")

    
    if FYERS_TOTP_SECRET:
        current_totp = pyotp.TOTP(FYERS_TOTP_SECRET).now()
        print(f"🔐 Your current TOTP is: {current_totp}")
        print("(Use this in the Fyers login page)\n")

    #Fyers Session setup
    session = fyersModel.SessionModel(
        client_id=FYERS_CLIENT_ID,
        secret_key=FYERS_SECRET_ID,
        redirect_uri=FYERS_REDIRECT_URL,
        response_type="code",
        grant_type="authorization_code"
    )

    #Generate Secure Login Link
    auth_link = session.generate_authcode()
    print("🌐 Fyers login page is opening in your browser...")
    
    # This will open the login URL in the default web browser
    webbrowser.open(auth_link)

    #Taking redirected URL input from user after login
    print("-" * 50)
    print("👉 After completing the login process, the blank page will show:")
    print("paste its url from the browser here:")
    redirected_url = input("\n🔗 Paste here: ")

    try:
        #Extracting auth code from the redirected URL
        parsed_url = urlparse(redirected_url)
        auth_code = parse_qs(parsed_url.query)['auth_code'][0]
        print(f"\n🎉 Found Auth Code: {auth_code}")

        #Extract final access token using the auth code
        session.set_token(auth_code)
        response = session.generate_token()
        
        if response.get('s') == 'ok':
            access_token = response['access_token']
            print("\n✅ SUCCESS! This is your ACCESS TOKEN:\n")
            print(access_token)
            print("\n(Paste this token in your .env file as FYERS_ACCESS_TOKEN=your_token_here)\n")
        else:
            print(f"❌ No token generated. Error: {response}")

    except Exception as e:
        print(f"❌ Error: There is a problem in generating the access token from the url, check whether the url is correct or not, Details: {e}")

if __name__ == "__main__":
    manual_login_flow()