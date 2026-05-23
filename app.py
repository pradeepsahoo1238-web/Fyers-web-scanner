import streamlit as st
from fyers_apiv3 import fyersModel
import pandas as pd

st.set_page_config(page_title="Sahoo Algo Terminal", layout="wide")

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
    st.title("🦅 Sahoo Advanced Algo Terminal")
    
    # Secrets से डेटा लेना
    client_id = st.secrets["FYERS_CLIENT_ID"]
    secret_key = st.secrets["FYERS_SECRET_KEY"]
    redirect_url = st.secrets["FYERS_REDIRECT_URL"]

    st.sidebar.header("📡 Market Connection")
    
    if st.sidebar.button("🔗 Connect Fyers Live"):
        # सुधरा हुआ सेशन मॉडल (नए अपडेट के साथ)
        session = fyersModel.SessionModel(
            client_id=client_id,
            secret_key=secret_key,
            redirect_url=redirect_url,
            response_type="code",
            grant_type="authorization_code"
        )
        auth_url = session.generate_auth_code()
        st.sidebar.link_button("👉 Click here to Login", auth_url)

    # डैशबोर्ड का हिस्सा
    tab1, tab2 = st.tabs(["🔥 लाइव स्कैनर", "📊 ऑप्शन चेन"])
    with tab1:
        st.subheader("Market Activity")
        st.write("Fyers से लॉगिन करने के बाद यहाँ लाइव डेटा रिफ्रेश होगा।")
        # यहाँ एक खाली टेबल ताकि स्क्रीन अच्छी दिखे
        df = pd.DataFrame({"Symbol": ["NIFTY", "BANKNIFTY"], "LTP": [0.0, 0.0]})
        st.table(df)
