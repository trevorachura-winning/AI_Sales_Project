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
    div[data-testid="stInfo"], div[data-testid="stSuccess"], div[data-testid="stWarning"] {
        border-radius: 10px;
        transition: transform 0.3s ease;
    }
    div[data-testid="stInfo"]:hover, div[data-testid="stSuccess"]:hover, div[data-testid="stWarning"]:hover {
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
    # Center the login box for better UI
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
# Sidebar Logout
if st.sidebar.button("🚪 Secure Logout", use_container_width=True):
    st.session_state['authenticated'] = False
    st.rerun()

st.sidebar.info("👉 **Next Step:** Select *Analytics Dashboard* above to begin.")

# Main Onboarding Content
st.title("🔥 Welcome to Flame AI-Sales")
st.markdown("### Your Enterprise Strategic Analytics & Intelligence Engine")
st.markdown("---")

# Section 1: About the Tool
st.header("💡 Platform Overview")
st.write("""
Flame AI-Sales transforms raw historical data into actionable foresight. By combining machine learning with dynamic data engineering, this platform allows you to forecast revenue, rank lead quality, and generate instant executive summaries without writing a single line of code.
""")

st.write("") # Spacer

# Section 2: How to Use It (Using Columns for layout)
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

# Section 3: Data Requirements
st.header("📋 Data Requirements for Success")
st.markdown("To ensure the AI engine generates accurate intelligence, your uploaded file must meet these criteria:")

req1, req2 = st.columns(2)
with req1:
    st.markdown("""
    * **File Format:** Must be a valid `.csv` file. 
    * **Clean Numbers:** Financial columns should be pure numbers (e.g., `350000`), completely free of currency symbols (`$`) or commas.
    * **Chronological Dates:** You must include at least one column formatted as a recognizable date (e.g., `YYYY-MM-DD` or `MM/DD/YYYY`).
    """)
with req2:
    st.markdown("""
    * **Categorical Data:** To use the Lead Scoring and Live Filter tools, include text-based categories (e.g., *Neighborhood, Acquisition Channel, or Product Tier*).
    * **Minimum Volume:** The Machine Learning algorithm requires a minimum of **6 chronological data points** to successfully train the predictive model, though 20+ rows are highly recommended for confident R-Squared validation.
    """)