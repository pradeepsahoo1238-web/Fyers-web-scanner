import hashlib

# ... upar ka session setup code wahi rahega ...

if st.button("Activate Session"):
    if auth_code:
        try:
            # 1. SHA256 Hash banana padta hai App_ID aur Secret_Key ka
            # Format: app_id + ":" + secret_key
            app_id_secret = f"{client_id}:{secret_key}"
            hash_result = hashlib.sha256(app_id_secret.encode()).hexdigest()

            # 2. Session mein token set karein
            session.set_token(auth_code)

            # 3. SAHI METHOD: generate_token() use karein (purana wala nahi)
            response = session.generate_token()

            if response.get("s") == "ok":
                st.session_state['access_token'] = response['access_token']
                st.success("✅ Logged In Successfully!")
                st.write("Aapka Access Token active hai.")
            else:
                st.error(f"Error from Fyers: {response.get('message')}")

        except Exception as e:
            st.error(f"Activation Failed: {e}")
    else:
        st.warning("Pehle Auth Code enter karein.")
