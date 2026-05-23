import streamlit as st
import pandas as pd
import time

# पेज सेटअप
st.set_page_config(page_title="Sahoo Terminal", layout="wide")

# लॉगिन की स्थिति चेक करना
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Sahoo Secure Login")
    # लॉगिन बॉक्स बनाना
    user_input = st.text_input("User ID")
    pass_input = st.text_input("Password", type="password")
    
    if st.button("टर्मिनल अनलॉक करें"):
        # यह 'तिजोरी' (Secrets) में लिखे डेटा से मिलान करेगा
        if user_input == st.secrets["MY_ID"] and pass_input == st.secrets["MY_PASSWORD"]:
            st.session_state.authenticated = True
            st.success("लॉगिन सफल!")
            st.rerun()
        else:
            st.error("गलत ID या पासवर्ड!")
else:
    # लॉगिन होने के बाद का नजारा
    st.title("🦅 Sahoo Advanced Trading Terminal")
    st.sidebar.success("Connected")
    if st.sidebar.button("Log Out"):
        st.session_state.authenticated = False
        st.rerun()

    # टैब्स
    t1, t2 = st.tabs(["🔥 स्कैनर", "📊 ऑप्शन चेन"])
    with t1:
        st.subheader("लाइव मार्केट स्कैनर")
        st.write("यहाँ आपका डेटा लोड हो रहा है...")
