import streamlit as st
from fyers_apiv3 import fyersModel
import hashlib

# --- CONFIGURATION ---
CLIENT_ID = "YOUR_APP_ID"  # Fyers Dashboard se lein
SECRET_KEY = "YOUR_SECRET_KEY" 
REDIRECT_URI = "https://fyers-web-scanner-jnk5fzyakjcfjueej3fcqg.streamlit.app/"

st.set_page_config(page_title="Fyers Web Scanner", layout="wide")
st.title("📊 Fyers Trading Dashboard")

# --- SESSION INITIALIZATION ---
if 'access_token' not in st.session_state:
    st.session_state.access_token = None

# Initialize Session Model
session = fyersModel.SessionModel(
    client_id=CLIENT_ID,
    secret_key=SECRET_KEY,
    redirect_uri=REDIRECT_URI,
    response_type='code',
    grant_type='authorization_code'
)

# --- LOGIN FLOW ---
if not st.session_state.access_token:
    if st.button("🔗 Step 1: Connect to Fyers"):
        try:
            # v3 Method: generate_authcode()
            auth_url = session.generate_authcode()
            st.markdown(f"### [👉 Yahan Click Karke Login Karein]({auth_url})")
        except Exception as e:
            st.error(f"Error: {e}")

    auth_code = st.text_input("Step 2: Login ke baad URL se 'auth_code' yahan paste karein:")
    
    if st.button("Step 3: Activate Session"):
        try:
            # v3 Requirement: Hash generation
            app_id_secret = f"{CLIENT_ID}:{SECRET_KEY}"
            hash_result = hashlib.sha256(app_id_secret.encode()).hexdigest()
            
            # Token set and generate
            session.set_token(auth_code)
            # SAHI METHOD: generate_token()
            response = session.generate_token()
            
            if response.get("s") == "ok":
                st.session_state.access_token = response['access_token']
                st.success("✅ Logged In Successfully!")
                st.rerun()
            else:
                st.error(f"Error: {response.get('message')}")
        except Exception as e:
            st.error(f"Activation Failed: {e}")

# --- TRADING DASHBOARD (After Login) ---
else:
    st.sidebar.success("⚡ Connected")
    st.write(f"Access Token: `{st.session_state.access_token[:10]}...`")
    
    if st.sidebar.button("Logout"):
        st.session_state.access_token = None
        st.rerun()

    # Yahan aap apna WebSocket ya Trading logic likh sakte hain
    st.subheader("Market Watch & WebSocket")
    st.info("Ab aap niche diye gaye code snippet ko use karke WebSocket data le sakte hain.")
