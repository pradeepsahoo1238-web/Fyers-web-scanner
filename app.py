import streamlit as st
from fyers_apiv3 import fyersModel

# 1. Page Config
st.set_page_config(page_title="Fyers Login", layout="centered")

# 2. Credentials (Yahan apni sahi details bharein)
client_id = "YOUR_APP_ID"  # Apna App ID yahan dalein
secret_key = "YOUR_SECRET_KEY" # Apna Secret Key yahan dalein
redirect_uri = "https://fyers-web-scanner-jnk5fzyakjcfjueej3fcqg.streamlit.app/"
st.title("🔗 Fyers Live Connection")

# 3. Session Initialize
session = fyersModel.SessionModel(
    client_id=client_id,
    secret_key=secret_key,
    redirect_uri=redirect_uri,
    response_type='code',
    grant_type='authorization_code'
)

# 4. Login Logic
if "auth_code" not in st.session_state:
    if st.button("Connect to Fyers"):
        try:
            # DHAYAN DEIN: Yahan 'generate_authcode' hai (v3 ka sahi spelling)
            response = session.generate_authcode()
            st.write("Niche diye link par click karke login karein:")
            st.markdown(f"[👉 Click Here to Login]({response})")
        except Exception as e:
            st.error(f"Error: {e}")

# 5. Token Generation (Login ke baad URL se code yahan dalna hoga)
auth_code_input = st.text_input("Login ke baad jo 'auth_code' mila use yahan paste karein:")
if st.button("Verify Account"):
    try:
        session.set_token(auth_code_input)
        access_token_resp = session.generate_access_token()
        st.success("✅ Login Successful!")
        st.write("Aapka Access Token: ", access_token_resp['access_token'])
    except Exception as e:
        st.error(f"Activation Failed: {e}")
