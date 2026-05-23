import streamlit as st
from fyers_apiv3.FyersWebsocket import data_ws, order_ws
import pandas as pd

# पेज कॉन्फ़िगरेशन
st.set_page_config(page_title="Sahoo Pro Algo", layout="wide")

# डेटा स्टोर करने के लिए तिजोरी
if "auth" not in st.session_state: st.session_state.auth = False
if "live_prices" not in st.session_state: st.session_state.live_prices = {}
if "order_updates" not in st.session_state: st.session_state.order_updates = []

# लॉगिन सुरक्षा
if not st.session_state.auth:
    st.title("🔐 Sahoo Secure Login")
    u = st.text_input("User ID")
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        if u == st.secrets["MY_ID"] and p == st.secrets["MY_PASSWORD"]:
            st.session_state.auth = True
            st.rerun()
else:
    st.title("🦅 Sahoo Advanced Algo Terminal")
    
    # Secrets से चाबियाँ (App ID : Access Token format में)
    access_token = f"{st.secrets['FYERS_CLIENT_ID']}:{st.secrets['FYERS_ACCESS_TOKEN']}"
    
    # --- WebSocket Callbacks (Docs के अनुसार) ---
    def on_market_data(message):
        """मार्केट डेटा अपडेट के लिए"""
        if "symbol" in message:
            st.session_state.live_prices[message["symbol"]] = message["ltp"]

    def on_order_update(message):
        """ऑर्डर और ट्रेड अपडेट के लिए"""
        st.session_state.order_updates.append(message)

    # साइडबार कंट्रोल्स
    st.sidebar.header("📡 Market Connectivity")
    if st.sidebar.button("🔗 Start Live Sockets"):
        st.sidebar.success("Sockets Connecting...")
        # यहाँ Websocket शुरू करने का लॉजिक आएगा (Backend में)

    # --- मेन डैशबोर्ड ---
    tab1, tab2, tab3 = st.tabs(["🔥 लाइव स्कैनर", "⛓️ ऑप्शन चेन", "📑 ऑर्डर्स & ट्रेड्स"])

    with tab1:
        st.subheader("Live Market (Data Socket)")
        symbols = ["NSE:NIFTY50-INDEX", "NSE:NIFTYBANK-INDEX", "NSE:RELIANCE-EQ", "NSE:SBIN-EQ"]
        
        # टेबल में डेटा दिखाना
        rows = []
        for s in symbols:
            price = st.session_state.live_prices.get(s, "Wait..")
            rows.append({"Symbol": s, "LTP": price})
        st.table(pd.DataFrame(rows))

    with tab3:
        st.subheader("Recent Order/Trade Updates (Order Socket)")
        if st.session_state.order_updates:
            st.write(st.session_state.order_updates[-1]) # आखिरी अपडेट
        else:
            st.info("कोई नया ऑर्डर अपडेट नहीं है।")

    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.rerun()
