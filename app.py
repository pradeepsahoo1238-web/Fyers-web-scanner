import streamlit as st
from fyers_apiv3 import fyersModel
import pandas as pd

# 1. पेज सेटअप
st.set_page_config(page_title="Sahoo Pro Algo", layout="wide")

# 2. लॉगिन सुरक्षा
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
            st.error("गलत लॉगिन डिटेल्स!")
else:
    st.title("🦅 Sahoo Advanced Algo Terminal")
    
    # Secrets से डेटा लेना
    cid = st.secrets["FYERS_CLIENT_ID"]
    skey = st.secrets["FYERS_SECRET_KEY"]
    rurl = st.secrets["FYERS_REDIRECT_URL"]

    st.sidebar.header("📡 Market Connection")
    
    # सुधरा हुआ लॉगिन लॉजिक: पहले बटन दबेगा, फिर लिंक दिखेगा
    if st.sidebar.button("🔗 Connect Fyers Live"):
        try:
            session = fyersModel.SessionModel(
                client_id=cid,
                secret_key=skey,
                redirect_uri=rurl,
                response_type="code"
            )
            auth_url = session.generate_auth_code()
            # यहाँ लिंक को एक बटन की तरह दिखा रहे हैं
            st.sidebar.markdown(f'''
                <a href="{auth_url}" target="_blank">
                    <button style="background-color: #ff4b4b; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; width: 100%;">
                        👉 Click here to Login Fyers
                    </button>
                </a>
            ''', unsafe_allow_html=True)
        except Exception as e:
            st.sidebar.error(f"Error: {e}")

    # डैशबोर्ड इंटरफेस
    tab1, tab2 = st.tabs(["🔥 लाइव स्कैनर", "📊 ऑप्शन चेन"])
    
    with tab1:
        st.subheader("Live Market Activity")
        st.info("Fyers लॉगिन के बाद डेटा लाइव अपडेट होगा।")
        df = pd.DataFrame({
            "Symbol": ["NIFTY 50", "BANK NIFTY", "RELIANCE", "SBIN"],
            "LTP": ["Wait..", "Wait..", "Wait..", "Wait.."]
        })
        st.table(df)

    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.rerun()
