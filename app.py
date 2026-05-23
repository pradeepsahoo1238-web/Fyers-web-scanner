import streamlit as st
from fyers_apiv3 import fyersModel
import pandas as pd

st.set_page_config(page_title="Sahoo Algo Terminal", layout="wide")

# 1. Authentication Check
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 Sahoo Secure Login")
    u = st.text_input("User ID")
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        if u == st.secrets["MY_ID"] and p == st.secrets["MY_PASSWORD"]:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Galat Details!")
else:
    # 2. Terminal Dashboard
    st.title("🦅 Sahoo Advanced Algo Terminal")
    
    # Secrets se data lena
    client_id = st.secrets["FYERS_CLIENT_ID"]
    secret_key = st.secrets["FYERS_SECRET_KEY"]
    redirect_url = st.secrets["FYERS_REDIRECT_URL"]

    st.sidebar.header("📡 Market Connection")
    
    # Is button ke click hone par hi Fyers link banega
    if st.sidebar.button("🔗 Connect Fyers Live"):
        session = fyersModel.SessionModel(
            client_id=client_id,
            secret_key=secret_key,
            redirect_url=redirect_url,
            response_type="code",
            grant_type="authorization_code"
        )
        auth_url = session.generate_auth_code()
        st.sidebar.success("Link Tayyar Hai!")
        st.sidebar.link_button("👉 Click here to Login to Fyers", auth_url)

    # Dashboard Interface
    tab1, tab2 = st.tabs(["🔥 लाइव स्कैनर", "📊 ऑप्शन चेन"])
    
    with tab1:
        st.subheader("Market Activity")
        st.info("Fyers se login karne ke baad data yahan dikhega.")
        # Khali table placeholder
        df = pd.DataFrame({"Symbol": ["NIFTY", "BANKNIFTY"], "LTP": [0.0, 0.0]})
        st.table(df)

    with tab2:
        st.subheader("Option Chain Analysis")
        st.write("Live OI data loading...")

    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.rerun()
