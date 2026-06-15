import streamlit as st

# --- Page Configuration ---
st.set_page_config(page_title="Enterprise Gateway", layout="centered")

# ==========================================
# 🔒 SECURE LOGIN GATEWAY
# ==========================================
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.title("🔒 Enterprise AI Analytics Workspace")
    st.markdown("Please enter your credentials to access the forecasting engine.")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Secure Login")
        
        if submit_button:
            if username == "admin" and password == "sales2026":
                st.session_state['authenticated'] = True
                st.success("Authentication successful! Loading workspace...")
                st.rerun()
            else:
                st.error("Invalid credentials. Please contact your system administrator.")
    st.stop() 

# ==========================================
# 👋 WELCOME SCREEN (Post-Login)
# ==========================================
st.title("👋 Welcome to the Analytics Workspace")
st.markdown("You have successfully authenticated.")
st.info("👈 Please select the **Analytics Dashboard** from the sidebar menu to begin forecasting.")

if st.sidebar.button("🚪 Logout"):
    st.session_state['authenticated'] = False
    st.rerun()