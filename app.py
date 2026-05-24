import streamlit as st
from fyers_apiv3.FyersWebsocket import data_ws
import pandas as pd
import time

# --- UI SETTINGS (HACKER STYLE) ---
st.set_page_config(page_title="Sahoo Vastu Algo", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #00ff41; }
    .stMetric { background-color: #1a1c24; border: 1px solid #00ff41; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ Dark Wave Algo-Terminal")

# --- SESSION STATE (कनेक्शन को टूटने से बचाने के लिए) ---
if 'live_data' not in st.session_state:
    st.session_state['live_data'] = {"NIFTY": 0, "BANKNIFTY": 0}

# --- FYERS CALLBACKS ---
def onmessage(message):
    # लाइव डेटा अपडेट करना
    symbol = message.get('symbol')
    ltp = message.get('ltp')
    if "NIFTY50" in symbol:
        st.session_state['live_data']["NIFTY"] = ltp
    elif "NIFTYBANK" in symbol:
        st.session_state['live_data']["BANKNIFTY"] = ltp

def onopen():
    symbols = ["NSE:NIFTY50-INDEX", "NSE:NIFTYBANK-INDEX"]
    fyers_socket.subscribe(symbols=symbols, data_type="SymbolUpdate")

# --- APP LOGIC ---
access_token = "YOUR_APP_ID:YOUR_ACCESS_TOKEN" # यहाँ अपना टोकन डालें

if st.button('Connect to Dark Wave'):
    with st.spinner('Establishing Socket Connection...'):
        fyers_socket = data_ws.FyersDataSocket(
            access_token=access_token,
            on_connect=onopen,
            on_message=onmessage,
            reconnect=True
        )
        fyers_socket.connect()
        st.success("Connected!")

# --- DASHBOARD LAYOUT ---
col1, col2 = st.columns(2)

with col1:
    st.metric(label="NIFTY 50", value=st.session_state['live_data']["NIFTY"])

with col2:
    st.metric(label="BANKNIFTY", value=st.session_state['live_data']["BANKNIFTY"])

# डेटा को रिफ्रेश करने के लिए छोटा सा लूप
if st.session_state['live_data']["NIFTY"] != 0:
    time.sleep(1)
    st.rerun()
