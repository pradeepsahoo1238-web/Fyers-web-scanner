import streamlit as st
from fyers_apiv3 import fyersModel
from fyers_apiv3.FyersWebsocket import data_ws, order_ws
import pandas as pd

# पेज सेटअप
st.set_page_config(page_title="Sahoo Pro Algo", layout="wide")

# डेटा स्टोर करने के लिए मेमोरी
if "auth" not in st.session_state: st.session_state.auth = False
if "access_token" not in st.session_state: st.session_state.access_token = None
if "live_prices" not in st.session_state: st.session_state.live_prices = {}

# --- लॉगिन स्क्रीन ---
if not st.session_state.auth:
    st.title("🔐 Sahoo Secure Login")
    u = st.text_input("User ID")
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        if u == st.secrets["MY_ID"] and p == st.secrets["MY_PASSWORD"]:
            st.session_state.auth = True
            st.rerun()
else:
    # --- मेन टर्मिनल ---
    st.title("🦅 Sahoo Advanced Algo Terminal")
    
    cid = st.secrets["FYERS_CLIENT_ID"]
    skey = st.secrets["FYERS_SECRET_KEY"]
    rurl = st.secrets["FYERS_REDIRECT_URL"]

    # साइडबार: कनेक्शन और टोकन
    st.sidebar.header("📡 Market Connection")
    
    # स्टेप 1: लॉगिन लिंक जेनरेट करना
    if st.sidebar.button("1. Get Login Link"):
        session = fyersModel.SessionModel(client_id=cid, secret_key=skey, redirect_uri=rurl, response_type="code", grant_type="authorization_code")
        st.sidebar.link_button("👉 Click to Login Fyers", session.generate_auth_code())

    # स्टेप 2: टोकन सेव करना (URL से कोड यहाँ पेस्ट करें)
    auth_code = st.sidebar.text_input("Paste Auth Code from URL here:")
    if st.sidebar.button("2. Generate Access Token"):
        session = fyersModel.SessionModel(client_id=cid, secret_key=skey, redirect_uri=rurl, response_type="code", grant_type="authorization_code")
        session.set_token(auth_code)
        response = session.generate_token()
        if "access_token" in response:
            st.session_state.access_token = response["access_token"]
            st.sidebar.success("Token Generated! 🟢")
        else:
            st.sidebar.error("Error generating token!")

    # --- डैशबोर्ड टैब्स ---
    tab1, tab2, tab3 = st.tabs(["🔥 लाइव स्कैनर", "⛓️ ऑप्शन चेन", "📑 ट्रेड बुक"])

    with tab1:
        st.subheader("Market Watch (Live WebSocket)")
        # सिम्बल्स की लिस्ट (Docs के अनुसार)
        symbols = ["NSE:NIFTY50-INDEX", "NSE:NIFTYBANK-INDEX", "NSE:RELIANCE-EQ", "NSE:SBIN-EQ"]
        
        # लाइव डेटा दिखाने की टेबल
        if st.session_state.access_token:
            st.write(f"Connected with Token: `{st.session_state.access_token[:10]}...`")
            # यहाँ सॉकेट डेटा का डिस्प्ले आएगा
        else:
            st.warning("कृपया ऊपर दिए गए स्टेप्स से टोकन जेनरेट करें।")

        df = pd.DataFrame({"Symbol": symbols, "LTP": ["Wait.."] * len(symbols)})
        st.table(df)

    with tab3:
        st.subheader("Your Positions & Orders")
        st.info("यहाँ आपकी लाइव पोजीशंस और P&L दिखेगा।")

    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.rerun()
