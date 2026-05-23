import streamlit as st
from fyers_apiv3 import fyersModel
import pandas as pd

st.set_page_config(page_title="Sahoo Algo Terminal", layout="wide")

# 1. Login Logic
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
    
    # Fyers Details from Secrets
    client_id = st.secrets["FYERS_CLIENT_ID"]
    secret_key = st.secrets["FYERS_SECRET_KEY"]
    redirect_url = st.secrets["FYERS_REDIRECT_URL"]

    st.sidebar.header("📡 Market Connection")
    
    # Fyers Login Button
    if st.sidebar.button("🔗 Connect Fyers Live"):
        session = fyersModel.SessionModel(
            client_id=client_id, 
            secret_key=secret_key, 
            redirect_url=redirect_url, 
            response_type="code", 
            grant_type="authorization_code"
        )
        auth_url = session.generate_auth_code()
        st.sidebar.info("Neeche diye link par click karke login karein:")
        st.sidebar.link_button("👉 Click here to Login", auth_url)

    # Main Tabs
    tab1, tab2 = st.tabs(["🔥 लाइव स्कैनर", "📊 ऑप्शन चेन"])
    
    with tab1:
        st.subheader("Live Market Volume Spikes")
        # Sample table for look
        data = {
            "Symbol": ["NIFTY 50", "BANK NIFTY", "RELIANCE", "SBIN"],
            "LTP": ["Loading...", "Loading...", "Loading...", "Loading..."],
            "Volume Shock": ["--", "--", "--", "--"]
        }
        st.table(pd.DataFrame(data))
        st.info("Fyers se login karne ke baad yahan live rates refresh honge.")

    with tab2:
        st.subheader("Option Chain (OI Analysis)")
        st.write("Nifty/BankNifty ki option chain yahan dikhegi.")
