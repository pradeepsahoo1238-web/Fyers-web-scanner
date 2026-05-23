import streamlit as st
from fyers_apiv3 import fyersModel
import pandas as pd

# 1. Page Config
st.set_page_config(page_title="Sahoo Algo Terminal", layout="wide")

# 2. Login Logic
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
            st.error("Invalid Login Details!")
else:
    st.title("🦅 Sahoo Advanced Algo Terminal")
    
    # Secrets से डेटा लेना
    cid = st.secrets["FYERS_CLIENT_ID"]
    skey = st.secrets["FYERS_SECRET_KEY"]
    rurl = st.secrets["FYERS_REDIRECT_URL"]

    st.sidebar.header("📡 Market Connection")
    
    # यहाँ 'redirect_uri' का इस्तेमाल किया गया है जो Fyers मांग रहा है
    if st.sidebar.button("🔗 Connect Fyers Live"):
        try:
            session = fyersModel.SessionModel(
                client_id=cid,
                secret_key=skey,
                redirect_uri=rurl,  # <--- यहाँ सुधार कर दिया गया है
                response_type="code",
                grant_type="authorization_code"
            )
            auth_url = session.generate_auth_code()
            st.sidebar.success("Link Tayyar!")
            st.sidebar.link_button("👉 Click here to Login to Fyers", auth_url)
        except Exception as e:
            st.sidebar.error(f"Technical Error: {e}")

    # Dashboard Tabs
    tab1, tab2 = st.tabs(["🔥 लाइव स्कैनर", "📊 ऑप्शन चेन"])
    
    with tab1:
        st.subheader("Live Market Activity")
        st.info("Fyers लॉगिन के बाद डेटा लोड होगा।")
        df = pd.DataFrame({
            "Symbol": ["NIFTY 50", "BANK NIFTY", "RELIANCE", "SBIN"],
            "LTP": ["Wait..", "Wait..", "Wait..", "Wait.."]
        })
        st.table(df)

    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.rerun()
