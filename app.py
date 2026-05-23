import streamlit as st
from fyers_apiv3 import fyersModel

# --- PAGE CONFIG ---
st.set_page_config(page_title="Fyers Trading Bridge", layout="centered")
st.title("📡 Fyers Live Connection v3")

# --- STEP 1: SECRETS SE DATA FETCH KARNA ---
# Streamlit Dashboard > Settings > Secrets mein ye keys honi chahiye
try:
    APP_ID = st.secrets["CLIENT_ID"]
    SECRET_KEY = st.secrets["SECRET_KEY"]
    REDIRECT_URI = st.secrets["REDIRECT_URI"]
except Exception as e:
    st.error("❌ Secrets Setup Missing!")
    st.info("""
    Streamlit Settings mein 'Secrets' box mein ye paste karein:
    
    CLIENT_ID = "YOUR_APP_ID"
    SECRET_KEY = "YOUR_SECRET_ID"
    REDIRECT_URI = "https://ej3fcqg.streamlit.app/"
    """)
    st.stop()

# --- STEP 2: SESSION INITIALIZATION ---
def get_session():
    return fyersModel.SessionModel(
        client_id=APP_ID,
        secret_key=SECRET_KEY,
        redirect_uri=REDIRECT_URI,
        response_type='code',
        grant_type='authorization_code'
    )

session = get_session()

# --- STEP 3: UI AND LOGIC ---
st.subheader("Connect Your Account")

if st.button("🔗 Generate Login Link"):
    try:
        # DHAYAN DEIN: 'generate_authcode' (v3 ka sahi method hai bina underscore ke)
        auth_url = session.generate_authcode()
        st.success("Login link ready hai!")
        st.markdown(f"### [👉 Yahan Click Karke Login Karein]({auth_url})")
        st.info("Login karne ke baad aap ek naye page par jayenge. Us page ke URL se 'auth_code=' ke baad wala hissa copy karein.")
    except Exception as e:
        st.error(f"Error: {e}")
        st.warning("Check karein: Kya Dashboard mein App ID sahi hai aur Status 'Active' hai?")

st.divider()

# --- STEP 4: ACCESS TOKEN GENERATION ---
auth_code = st.text_input("Yahan 'auth_code' paste karein:")

if st.button("⚡ Activate Connection"):
    if auth_code:
        try:
            session.set_token(auth_code)
            response = session.generate_access_token()
            
            if response.get('s') == 'ok':
                st.session_state['access_token'] = response.get('access_token')
                st.success("🎉 Mubarak ho! Aapka Fyers App Active ho gaya hai.")
                st.balloons()
            else:
                st.error(f"Token error: {response.get('message')}")
        except Exception as e:
            st.error(f"Failed to activate: {e}")
    else:
        st.warning("Pehle login karke auth_code layein.")

# --- STEP 5: STATUS CHECK ---
if 'access_token' in st.session_state:
    st.sidebar.success("✅ App Status: Online")
    if st.sidebar.button("Logout"):
        del st.session_state['access_token']
        st.rerun()
else:
    st.sidebar.error("❌ App Status: Offline")
