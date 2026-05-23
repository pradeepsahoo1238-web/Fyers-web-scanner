import streamlit as st
from fyers_apiv3 import fyersModel
import pandas as pd

# पेज सेटिंग्स
st.set_page_config(page_title="Sahoo Algo Terminal", layout="wide")

# 1. सुरक्षा लॉगिन
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
            st.error("गलत क्रेडेंशियल्स!")
else:
    # 2. मुख्य टर्मिनल
    st.title("🦅 Sahoo Advanced Algo Terminal")
    
    # Secrets से चाबियां लेना
    cid = st.secrets["FYERS_CLIENT_ID"]
    skey = st.secrets["FYERS_SECRET_KEY"]
    rurl = st.secrets["FYERS_REDIRECT_URL"]

    st.sidebar.header("📡 Market Connection")
    
    # Fyers कनेक्ट करने का बटन
    if st.sidebar.button("🔗 Connect Fyers Live"):
        try:
            session = fyersModel.SessionModel(
                client_id=cid,
                secret_key=skey,
                redirect_url=rurl,
                response_type="code",
                grant_type="authorization_code"
            )
            auth_url = session.generate_auth_code()
            st.sidebar.success("लिंक तैयार है!")
            st.sidebar.link_button("👉 Click here to Login to Fyers", auth_url)
        except Exception as e:
            st.sidebar.error(f"Setup Error: {e}")

    # डैशबोर्ड लेआउट
    t1, t2 = st.tabs(["🔥 लाइव स्कैनर", "📊 ऑप्शन चेन"])
    
    with t1:
        st.subheader("Live Market Activity")
        st.info("Fyers लॉगिन के बाद यहाँ डेटा लाइव अपडेट होगा।")
        # डेटा टेबल का ढांचा
        df = pd.DataFrame({
            "Symbol": ["NIFTY 50", "BANK NIFTY", "RELIANCE", "SBIN"],
            "LTP": ["Wait..", "Wait..", "Wait..", "Wait.."],
            "Volume": ["--", "--", "--", "--"]
        })
        st.table(df)

    with t2:
        st.subheader("Option Chain Data")
        st.write("Live OI Analysis loading...")

    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.rerun()
