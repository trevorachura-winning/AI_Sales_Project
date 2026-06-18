import streamlit as st

# --- Page Configuration ---
st.set_page_config(page_title="Flame AI-Sales Gateway", page_icon="🔥", layout="wide")

# --- Initialize Security State ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# ==========================================
# 🔒 STATE 1: THE LOGIN GATEWAY
# ==========================================
if not st.session_state['authenticated']:
    # MAGIC TRICK: Hide the sidebar and style the login box to look like a SaaS landing page
    st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none; } /* Hides sidebar */
        .block-container { max-width: 800px; padding-top: 5rem; animation: fadeIn 0.8s; }
        @keyframes fadeIn { 0% { opacity: 0; } 100% { opacity: 1; } }
        div[data-testid="stForm"] {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 35px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; font-size: 3.5rem;'>🔥 Flame AI-Sales</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; font-size: 1.2rem; margin-bottom: 2rem;'>Enterprise Strategic Analytics & Intelligence Engine</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        with st.form("login_form"):
            st.markdown("### 🔒 Secure System Access")
            username = st.text_input("Username", placeholder="Enter official username")
            password = st.text_input("Password", type="password", placeholder="Enter access key")
            submit_button = st.form_submit_button("Authenticate System", use_container_width=True)
            
            if submit_button:
                if username == "user" and password == "sales2026":
                    st.session_state['authenticated'] = True
                    st.rerun() # Instantly reloads the page to reveal the Welcome Screen
                else:
                    st.error("Invalid credentials. Please contact your system administrator.")
    st.stop() # Completely stops the rest of the page from rendering until logged in

# ==========================================
# 🎉 STATE 2: THE WELCOME & ONBOARDING SCREEN
# ==========================================
# CSS specifically for the Onboarding screen
st.markdown("""
<style>
    .block-container { animation: fadeInUp 0.6s ease-out; max-width: 1200px; }
    @keyframes fadeInUp { 0% { opacity: 0; transform: translateY(15px); } 100% { opacity: 1; transform: translateY(0); } }
    div[data-testid="stInfo"]:hover, div[data-testid="stSuccess"]:hover, div[data-testid="stWarning"]:hover {
        transform: translateY(-3px); transition: transform 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# The sidebar is now visible!
st.sidebar.success("✅ **Authentication Successful**")
st.sidebar.info("👉 **Next Step:** Select *Analytics Dashboard* above to begin forecasting.")

st.title("🔥 Welcome to Flame AI-Sales")
st.markdown("### Your Enterprise Strategic Analytics & Intelligence Engine")
st.markdown("---")

# Section 1: About the Tool
st.header("💡 Platform Overview")
st.write("Flame AI-Sales transforms raw historical data into actionable foresight. By combining machine learning with dynamic data engineering, this platform allows you to forecast revenue, rank lead quality, and generate instant executive summaries.")

st.write("") 

# Section 2: How to Use It
st.header("🛠️ Workflow Guide")
step1, step2, step3 = st.columns(3)
with step1:
    st.info("**Step 1: Data Ingestion**\n\nNavigate to the **Analytics Dashboard** via the left sidebar menu and upload your historical CSV file. The engine will instantly map your data into RAM.")
with step2:
    st.warning("**Step 2: Schema Alignment**\n\nUse the sidebar dropdowns to tell the AI how to read your data. Select the column that represents your **Timeline (Dates)** and the column representing your **Target (Revenue/Sales)**.")
with step3:
    st.success("**Step 3: Strategic Extraction**\n\nClick through the interactive workspace tabs to view automated AI forecasts, calculate dynamic lead scores, and read AI-generated strategic next steps.")

st.write("---")

# Section 3: AI Algorithms Explained
st.header("🧠 AI Algorithms Explained")
st.markdown("The engine allows you to select from several predictive algorithms. Here is a guide to what they achieve:")

alg1, alg2 = st.columns(2)
with alg1:
    st.info("**📉 Linear Regression:** The most fundamental model. It looks for a simple, straight-line relationship over time. Best used for highly stable, predictable data without massive spikes.")
    st.success("**🌲 Decision Tree:** This model splits data into branches based on strict conditions. Good for datasets driven by clear categories.")
with alg2:
    st.warning("**🌳 Random Forest:** An advanced ensemble model that builds hundreds of Decision Trees and averages their predictions. Extremely reliable, as it prevents the AI from 'overfitting' or memorizing anomalies.")
    st.error("**🚀 Gradient Boosting:** Our most powerful forecasting model. It trains sequentially—meaning each new tree specifically focuses on fixing the errors of the previous one. Highly accurate for complex, fluctuating sales cycles.")

st.write("---")

# Section 4: Data Requirements
st.header("📋 Data Requirements for Success")
req1, req2 = st.columns(2)
with req1:
    st.markdown("* **File Format:** Must be a valid `.csv` file. \n* **Clean Numbers:** Financial columns should be pure numbers (e.g., `350000`), completely free of currency symbols (`$`) or commas.\n* **Chronological Dates:** You must include at least one column formatted as a recognizable date.")
with req2:
    st.markdown("* **Categorical Data:** To use the Lead Scoring and Live Filter tools, include text-based categories.\n* **Minimum Volume:** The AI requires a minimum of **6 chronological data points** to train, though 20+ rows are highly recommended.")

# Global Logout Button
st.sidebar.markdown("<br>" * 10, unsafe_allow_html=True) 
if st.sidebar.button("🚪 Secure Logout", use_container_width=True, key="home_logout"):
    st.session_state['authenticated'] = False
    st.rerun()