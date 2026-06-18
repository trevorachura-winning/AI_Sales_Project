import streamlit as st

# --- Page Configuration ---
st.set_page_config(page_title="Flame AI-Sales Gateway", layout="wide")

# ==========================================
# 🎨 CUSTOM UI INJECTION FOR HOME PAGE
# ==========================================
st.markdown("""
<style>
    .block-container { animation: fadeInUp 0.8s ease-out; }
    @keyframes fadeInUp { 0% { opacity: 0; transform: translateY(20px); } 100% { opacity: 1; transform: translateY(0); } }
    div[data-testid="stInfo"], div[data-testid="stSuccess"], div[data-testid="stWarning"], div[data-testid="stError"] {
        border-radius: 10px;
        transition: transform 0.3s ease;
    }
    div[data-testid="stInfo"]:hover, div[data-testid="stSuccess"]:hover, div[data-testid="stWarning"]:hover, div[data-testid="stError"]:hover {
        transform: translateY(-5px);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🔒 SECURE LOGIN GATEWAY
# ==========================================
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🔥 Flame AI-Sales")
        st.markdown("Please enter your official credentials to access the forecasting engine.")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Secure Login", use_container_width=True)
            
            if submit_button:
                if username == "user" and password == "sales2026":
                    st.session_state['authenticated'] = True
                    st.success("Authentication successful! Loading workspace...")
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please contact your system administrator.")
    st.stop() 

# ==========================================
# 👋 PLATFORM ONBOARDING (Post-Login)
# ==========================================

st.sidebar.info("👉 **Next Step:** Select *Analytics Dashboard* above to begin.")

st.title("🔥 Welcome to Flame AI-Sales")
st.markdown("### Your Enterprise Strategic Analytics & Intelligence Engine")
st.markdown("---")

# Section 1: About the Tool
st.header("💡 Platform Overview")
st.write("""
Flame AI-Sales transforms raw historical data into actionable foresight. By combining machine learning with dynamic data engineering, this platform allows you to forecast revenue, rank lead quality, and generate instant executive summaries.
""")

st.write("") # Spacer

# Section 2: How to Use It
st.header("🛠️ Workflow Guide")
step1, step2, step3 = st.columns(3)

with step1:
    st.info("""
    **Step 1: Data Ingestion**
    
    Navigate to the **Analytics Dashboard** via the left sidebar menu and upload your historical CSV file. The engine will instantly map your data into RAM.
    """)

with step2:
    st.warning("""
    **Step 2: Schema Alignment**
    
    Use the sidebar dropdowns to tell the AI how to read your data. Select the column that represents your **Timeline (Dates)** and the column representing your **Target (Revenue/Sales)**.
    """)

with step3:
    st.success("""
    **Step 3: Strategic Extraction**
    
    Click through the interactive workspace tabs to view automated AI forecasts, calculate dynamic lead scores, and read AI-generated strategic next steps.
    """)

st.write("---")

# Section 3: AI Algorithms Explained
st.header("🧠 AI Algorithms Explained")
st.markdown("The engine allows you to select from several predictive algorithms. Here is a guide to what they achieve:")

alg1, alg2 = st.columns(2)
with alg1:
    st.info("**📉 Linear Regression:** The most fundamental model. It looks for a simple, straight-line relationship over time. Best used for highly stable, predictable data without massive spikes.")
    st.success("**🌲 Decision Tree:** This model splits data into branches based on strict conditions (e.g., *'If neighborhood is Urban, predict X'*). Good for datasets driven by clear categories.")
with alg2:
    st.warning("**🌳 Random Forest:** An advanced ensemble model that builds hundreds of Decision Trees and averages their predictions. Extremely reliable, as it prevents the AI from 'overfitting' or memorizing anomalies.")
    st.error("**🚀 Gradient Boosting:** Our most powerful forecasting model. It trains sequentially—meaning each new tree specifically focuses on fixing the errors of the previous one. Highly accurate for complex, fluctuating sales cycles.")

st.write("---")

# Section 4: Data Requirements
st.header("📋 Data Requirements for Success")
req1, req2 = st.columns(2)
with req1:
    st.markdown("""
    * **File Format:** Must be a valid `.csv` file. 
    * **Clean Numbers:** Financial columns should be pure numbers (e.g., `350000`), completely free of currency symbols (`$`) or commas.
    * **Chronological Dates:** You must include at least one column formatted as a recognizable date.
    """)
with req2:
    st.markdown("""
    * **Categorical Data:** To use the Lead Scoring and Live Filter tools, include text-based categories (e.g., *Acquisition Channel, or Product Tier*).
    * **Minimum Volume:** The AI requires a minimum of **6 chronological data points** to train, though 20+ rows are highly recommended.
    """)

# Global Logout Button (Pushed to bottom of sidebar)
st.sidebar.markdown("<br>" * 10, unsafe_allow_html=True) # Adds invisible spacing to push the button down
if st.sidebar.button("🚪 Secure Logout", use_container_width=True, key="home_logout"):
    st.session_state['authenticated'] = False
    st.rerun()