import streamlit as st
from fyers_apiv3 import fyersModel

# --- AAPKI DETAILS ---
APP_ID = "UWOFOLR5NU-100"  # Aapki exact App ID
SECRET_ID = "GHR2A71FAH"    # Aapki exact Secret ID
REDIRECT_URI = "https://ej3fcqg.streamlit.app/" # Ensure this matches Fyers Dashboard exactly

st.set_page_config(page_title="Fyers Trading Bot", layout="centered")
st.title("📡 Fyers Market Connection")

# Session Initialize
session = fyersModel.SessionModel(
    client_id=APP_ID,
    secret_key=SECRET_ID,
    redirect_uri=REDIRECT_URI,
    response_type='code',
    grant_type='authorization_code'
)

# UI Layout
if st.button("🔗 Connect Fyers Live"):
    try:
        # Step 1: Generate Login Link
        # v3 mein 'generate_authcode' (bina underscore) sabse stable hai
        auth_url = session.generate_authcode()
        st.success("Login link ready hai!")
        st.markdown(f"### [👉 Yahan Click Karein Login Ke Liye]({auth_url})")
    except Exception as e:
        st.error(f"Error: {e}")

st.divider()

# Step 2: Auth Code Input
auth_code = st.text_input("Login ke baad URL mein se 'auth_code' copy karke yahan paste karein:")

if st.button("Verify & Activate"):
    if auth_code:
        try:
            session.set_token(auth_code)
            response = session.generate_access_token()
            access_token = response['access_token']
            st.session_state['access_token'] = access_token
            st.success("✅ App Active ho gayi hai! Aap connect ho chuke hain.")
        except Exception as e:
            st.error(f"Activation Failed: {e}")
    else:
        st.warning("Pehle login karke auth_code layein.")
