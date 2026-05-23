import streamlit as st
from fyers_apiv3 import fyersModel
import webbrowser

# --- CONFIGURATION ---
# Inhe aap apne Fyers Dashboard (api-t1.fyers.in) se le sakte hain
CLIENT_ID = "YOUR_CLIENT_ID_HERE" 
SECRET_KEY = "YOUR_SECRET_KEY_HERE"
REDIRECT_URI = "https://ej3fcqg.streamlit.app/" # Ensure this matches exactly in Fyers Dashboard

st.set_page_config(page_title="Fyers Trading Bot", layout="centered")

st.title("📡 Market Connection")
st.divider()

# --- SESSION INITIALIZATION ---
if 'access_token' not in st.session_state:
    st.session_state.access_token = None

# Initialize SessionModel
session = fyersModel.SessionModel(
    client_id=CLIENT_ID,
    secret_key=SECRET_KEY,
    redirect_uri=REDIRECT_URI,
    response_type='code',
    grant_type='authorization_code'
)

# --- UI LOGIC ---
if not st.session_state.access_token:
    st.info("Aapka account connected nahi hai. Please login karein.")
    
    if st.button("🔗 Connect Fyers Live"):
        try:
            # DHAYAN DEIN: 'generate_authcode' (v3 ka sahi method hai)
            auth_url = session.generate_authcode()
            
            st.success("Login link generate ho gaya hai!")
            st.markdown(f"### [👉 Yahan Click Karke Login Karein]({auth_url})")
            st.caption("Login karne ke baad aap redirect honge, wahan se 'auth_code' copy karke niche dalein.")
            
        except Exception as e:
            st.error(f"Error generating link: {e}")

    # Auth Code se Access Token banane ka section
    auth_code = st.text_input("Login ke baad URL se 'auth_code' yahan paste karein:")
    
    if st.button("Verify & Activate"):
        if auth_code:
            try:
                session.set_token(auth_code)
                response = session.generate_access_token()
                st.session_state.access_token = response['access_token']
                st.success("✅ Connection Successful! Ab aap trading kar sakte hain.")
                st.rerun()
            except Exception as e:
                st.error(f"Activation Error: {e}")
        else:
            st.warning("Please enter the auth code first.")

else:
    st.success("⚡ Connected to Fyers Live")
    if st.button("Logout"):
        st.session_state.access_token = None
        st.rerun()

# --- REQUIREMENTS FILE KA CONTENT ---
# Ye aapko 'requirements.txt' naam ki file mein daalna hai GitHub par:
"""
# requirements.txt content:
# streamlit
# fyers-apiv3
# pandas
"""
