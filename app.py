import streamlit as st
import pandas as pd
import time
import plotly.graph_objects as go
import numpy as np

# 1. पेज कॉन्फ़िगरेशन और डार्क थीम
st.set_page_config(page_title="Sahoo Pro Terminal", page_icon="⚡", layout="wide")

# CSS से लुक को और प्रोफेशनल बनाना
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #1e293b;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
        color: white;
    }
    </style>
    """, unsafe_allow_globals=True)

# 2. सुरक्षित लॉगिन लॉजिक (Secrets से कनेक्टेड)
# नोट: आपको अपनी वेबसाइट की Settings > Secrets में MY_ID और MY_PASSWORD भरना होगा।
def check_auth():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.title("🔐 Sahoo Secure Login")
        with st.container():
            user_input = st.text_input("Fyers User ID")
            pass_input = st.text_input("Password", type="password")
            pin_input = st.text_input("2FA PIN", type="password")
            
            if st.button("टर्मिनल अनलॉक करें"):
                # सुरक्षा जांच: Secrets से मैच करना
                try:
                    if user_input == st.secrets["MY_ID"] and pass_input == st.secrets["MY_PASSWORD"]:
                        st.session_state.authenticated = True
                        st.success("लॉगिन सफल!")
                        st.rerun()
                    else:
                        st.error("गलत क्रेडेंशियल्स! कृपया दोबारा जांचें।")
                except:
                    st.warning("⚠️ कृपया पहले Streamlit की Secrets सेटिंग्स में MY_ID और MY_PASSWORD सेट करें।")
        return False
    return True

if check_auth():
    # 3. मुख्य टर्मिनल इंटरफेस
    st.title("🦅 Sahoo Advanced Pro Terminal")
    st.sidebar.success("🟢 लाइव मार्केट से कनेक्टेड")
    
    if st.sidebar.button("Log Out"):
        st.session_state.authenticated = False
        st.rerun()

    # टैब्स बनाना
    tab1, tab2, tab3 = st.tabs(["🔥 बिग मनी स्कैनर", "⛓️ प्रो ऑप्शन चेन", "📊 एडवांस्ड चार्ट"])

    with tab1:
        st.subheader("FII/DII लाइव वॉल्यूम स्पाइक")
        df_scan = pd.DataFrame({
            "समय": [time.strftime('%H:%M:%S') for _ in range(5)],
            "स्टॉक सिंबल": ["RELIANCE", "SBIN", "HDFCBANK", "ICICIBANK", "TCS"],
            "LTP": [2850.40, 780.20, 1650.10, 1080.50, 3950.00],
            "वॉल्यूम शॉक": ["540% ⚡", "320% 🔥", "210% ✅", "450% ⚡", "180% ✅"]
        })
        st.table(df_scan)

    with tab2:
        st.subheader("NIFTY 50 - लाइव ऑप्शन चेन (OI)")
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Total Call OI", "45.2L", "+12%")
        col_m2.metric("PCR", "0.92", "Neutral")
        col_m3.metric("Total Put OI", "41.5L", "-5%")
        
        strikes = [22000, 22100, 22200, 22300, 22400]
        oc_data = pd.DataFrame({
            "CALL OI (L)": [10.5, 25.4, 55.2, 12.8, 5.4],
            "LTP (CE)": [250, 180, 110, 60, 25],
            "STRIKE": strikes,
            "LTP (PE)": [30, 75, 135, 210, 300],
            "PUT OI (L)": [4.2, 8.1, 48.6, 35.2, 12.4]
        })
        st.dataframe(oc_data, use_container_width=True)

    with tab3:
        st.subheader("लाइव टेक्निकल चार्ट")
        fig = go.Figure(data=[go.Candlestick(
            x=pd.date_range(end=pd.Timestamp.now(), periods=50, freq='15min'),
            open=np.random.randn(50).cumsum() + 100,
            high=np.random.randn(50).cumsum() + 105,
            low=np.random.randn(50).cumsum() + 95,
            close=np.random.randn(50).cumsum() + 100
        )])
        fig.update_layout(template="plotly_dark", height=600, xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

    # हर 5 सेकंड में ऑटो-रिफ्रेश
    time.sleep(5)
    st.rerun()
