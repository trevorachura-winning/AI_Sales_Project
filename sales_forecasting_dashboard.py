import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# --- Page Configuration ---
st.set_page_config(page_title="Universal AI Forecasting Engine", layout="wide")
# --- Page Configuration ---
st.set_page_config(page_title="Universal AI Forecasting Engine", layout="wide")

# ==========================================
# 🔒 PHASE 2: SECURE LOGIN GATEWAY
# ==========================================
# 1. Check if the user is already logged in
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# 2. Build the Login UI if they are NOT logged in
if not st.session_state['authenticated']:
    st.title("🔒 Enterprise AI Analytics Workspace")
    st.markdown("Please enter your organizational credentials to access the forecasting engine.")
    
    # Create a visual box for the login form
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password") # Hides the text as dots
        submit_button = st.form_submit_button("Secure Login")
        
        if submit_button:
            # Check the credentials (you can change these later!)
            if username == "admin" and password == "sales2026":
                st.session_state['authenticated'] = True
                st.success("Authentication successful! Loading workspace...")
                st.rerun() # Instantly refreshes the page to reveal the dashboard
            else:
                st.error("Invalid credentials. Please contact your system administrator.")
    
    # 3. THE BOUNCER: Stop the rest of the code from running
    st.stop() 


# ==========================================
# 📈 PHASE 3: THE MAIN DASHBOARD
# ==========================================
# (If the code reaches here, it means they logged in successfully!)

# Add a logout button to the sidebar
if st.sidebar.button("🚪 Logout"):
    st.session_state['authenticated'] = False
    st.rerun()

st.title("🤖 Universal AI Forecasting & Analytics Engine")
st.markdown("Upload **any** historical time-series dataset. The system will auto-detect columns, handle data engineering, and train your chosen AI model dynamically.")

# --- File Ingestion ---
# ... (THE REST OF YOUR EXISTING UPLOAD AND AI CODE STAYS EXACTLY THE SAME BELOW THIS LINE) ...
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=['csv'])
st.title("🤖 Universal AI Forecasting & Analytics Engine")
st.markdown("Upload **any** historical time-series dataset. The system will auto-detect columns, handle data engineering, and train your chosen AI model dynamically.")

# --- File Ingestion ---
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=['csv'])

if uploaded_file is not None:
    # Read file
    df = pd.read_csv(uploaded_file)
    
    st.write(f"### 📋 Raw Dataset Preview ({len(df)} rows × {len(df.columns)} columns)")
    st.dataframe(df.head(5))

    st.sidebar.markdown("---")
    st.sidebar.header("🎛️ Schema Alignment")

    # 1. DYNAMIC DATE DETECTION (UPDATED: Bulletproof Pandas 2.0 compatibility)
    date_options = []
    for col in df.columns:
        # Check if Pandas already securely knows it is a datetime column
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            date_options.append(col)
        # Check if it is text/string that can safely be parsed into a date
        elif pd.api.types.is_string_dtype(df[col]) or df[col].dtype == 'object':
            try:
                # Test parse first 5 rows to see if it's a date format
                pd.to_datetime(df[col].head(5))
                date_options.append(col)
            except:
                pass

    if not date_options:
        st.error("No Date/Timeline columns could be detected. Please ensure your CSV has a valid date column.")
        st.stop()

    # Let user confirm or choose the correct date column
    date_col = st.sidebar.selectbox("Select Timeline/Date Column", options=date_options, index=0)
    
    # Standardize selected date column
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df = df.dropna(subset=[date_col]).sort_values(by=date_col)

    # 2. TARGET SELECTION (What do we want to forecast?)
    # Filter for numeric columns as forecasting targets
    numeric_cols = list(df.select_dtypes(include=[np.number]).columns)
    
    if not numeric_cols:
        st.error("No numerical columns found in your dataset to forecast. Please check your data.")
        st.stop()

    target_col = st.sidebar.selectbox("Select Target Column to Forecast", options=numeric_cols, 
                                      index=len(numeric_cols)-1 if len(numeric_cols) > 1 else 0)

    # 3. DYNAMIC CATEGORICAL FILTERS
    st.sidebar.markdown("---")
    st.sidebar.header("📊 Dashboard Live Filters")
    
    # Identify high-value categorical filters (text columns with realistic cardinality)
    categorical_cols = list(df.select_dtypes(include=['object', 'category', 'string']).columns)
    if date_col in categorical_cols:
        categorical_cols.remove(date_col)

    # Automatically construct live UI filters based on what exists in the file
    filtered_df = df.copy()
    
    # Limit to top 3 categorical columns to avoid overwhelming the sidebar UI
    for col in categorical_cols[:3]:
        unique_vals = ['All'] + list(df[col].dropna().unique())
        selected_val = st.sidebar.selectbox(f"Filter by {col}", unique_vals)
        if selected_val != 'All':
            filtered_df = filtered_df[filtered_df[col] == selected_val]

    # --- DATAFRAME CLEANING & FEATURE SELECTION ---
    # Automatic feature engineering based on dates
    filtered_df['Engine_Month'] = filtered_df[date_col].dt.month
    filtered_df['Engine_DayOfWeek'] = filtered_df[date_col].dt.dayofweek
    filtered_df['Engine_IsWeekend'] = filtered_df[date_col].dt.dayofweek >= 5

    # Fill NaNs globally depending on types safely
    for col in filtered_df.columns:
        if pd.api.types.is_numeric_dtype(filtered_df[col]):
            filtered_df[col] = filtered_df[col].fillna(0)
        else:
            filtered_df[col] = filtered_df[col].fillna("Unknown")

    # --- DYNAMIC VISUALIZATIONS ---
    st.write("### 📈 Automated Data Exploration")
    v_col1, v_col2 = st.columns(2)

    with v_col1:
        st.write(f"**Timeline Trend: Average {target_col} Over Time**")
        fig_time, ax_time = plt.subplots(figsize=(7, 3.5))
        time_series = filtered_df.groupby(filtered_df[date_col].dt.to_period('M'))[target_col].mean()
        time_series.index = time_series.index.astype(str)
        ax_time.plot(time_series.index, time_series.values, marker='o', color='#1f77b4')
        ax_time.tick_params(axis='x', rotation=45)
        st.pyplot(fig_time)

    with v_col2:
        if len(categorical_cols) > 0:
            primary_cat = categorical_cols[0]
            st.write(f"**Distribution: Proportional {target_col} by {primary_cat}**")
            fig_pie, ax_pie = plt.subplots(figsize=(7, 3.5))
            cat_group = filtered_df.groupby(primary_cat)[target_col].sum().reset_index()
            ax_pie.pie(cat_group[target_col], labels=cat_group[primary_cat], autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
            ax_pie.axis('equal')
            st.pyplot(fig_pie)
        else:
            st.info("Upload data containing string columns to unlock distribution graphs.")

    # --- ML AUTOMATION PIPELINE ---
    st.write("---")
    st.sidebar.markdown("---")
    st.sidebar.header("🤖 Model Configurations")
    model_choice = st.sidebar.selectbox("Choose Learning Algorithm", 
        ["Gradient Boosting", "Random Forest", "Linear Regression", "Decision Tree"])

    st.write(f"### 🔮 AI Predictive Analytics Model: {model_choice}")

    # Prepare data for AI without referencing hardcoded text keys
    # Dynamically extract tracking variables
    ml_features_df = filtered_df.drop(columns=[date_col, target_col], errors='ignore')
    
    # Automatically convert whatever categorical features exist into dynamic One-Hot matrix columns
    ml_encoded = pd.get_dummies(ml_features_df, drop_first=True)
    
    # Clear out structural strings or IDs that cannot map to weights
    X = ml_encoded.select_dtypes(include=[np.number, bool])
    y = filtered_df[target_col]

    if len(X) > 5:  # Lowered threshold slightly for smaller datasets like our SaaS sample
        # Train-Test Split (sequential for chronological accuracy)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)

        if model_choice == "Gradient Boosting":
            model = GradientBoostingRegressor(random_state=42)
        elif model_choice == "Random Forest":
            model = RandomForestRegressor(random_state=42)
        elif model_choice == "Linear Regression":
            model = LinearRegression()
        else:
            model = DecisionTreeRegressor(random_state=42)

        # Train and Forecast
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        
        # Performance Evaluation Metrics
        mae = mean_absolute_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)

        m_col1, m_col2 = st.columns(2)
        m_col1.metric("Mean Absolute Error (MAE)", f"{mae:.2f}")
        m_col2.metric("R-Squared (Explaining Variance)", f"{r2:.2f}")

        # Plot Forecast Validation Line Chart
        fig_forecast, ax_forecast = plt.subplots(figsize=(14, 4))
        ax_forecast.plot(range(len(y_test)), y_test.values, label='Actual Historical Values', color='orange', alpha=0.8, marker='o')
        ax_forecast.plot(range(len(predictions)), predictions, label='AI Forecast Path', color='green', linestyle='--', alpha=0.8, marker='x')
        ax_forecast.set_title("AI Predictive Tracking Verification Validation Curve")
        ax_forecast.set_xlabel("Sequential Chronological Testing Timeline (Unseen Test Block)")
        ax_forecast.set_ylabel(target_col)
        ax_forecast.legend()
        st.pyplot(fig_forecast)
    else:
        st.warning("Insufficient variation entries available to optimize AI modeling matrices. Upload a dataset with more rows to augment sample row quantities.")

else:
    st.info("🔌 Awaiting system payload connection. Drop an engineering log file template into the sidebar interface to initiate model optimization modules.")