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
from sklearn.preprocessing import MinMaxScaler

st.set_page_config(page_title="Strategic Analytics Dashboard", layout="wide")

# --- Security Check ---
if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
    st.warning("🛑 Access Denied. Please log in through the main Gateway page first.")
    st.stop()

# --- THE MAIN DASHBOARD ---
st.title("📊 Strategic Analytics & Intelligence Engine")
st.markdown("Upload your dataset to generate AI forecasts, rank lead quality, and extract automated executive summaries.")

uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=['csv'], key="unique_data_uploader")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    st.sidebar.markdown("---")
    st.sidebar.header("🎛️ Schema Alignment")

    # 1. Date Detection
    date_options = [col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col])]
    if not date_options:
        for col in df.columns:
            if pd.api.types.is_string_dtype(df[col]) or df[col].dtype == 'object':
                try:
                    pd.to_datetime(df[col].head(3))
                    date_options.append(col)
                except:
                    pass

    if not date_options:
        st.error("No Date/Timeline columns detected. Please ensure your CSV has a valid date column.")
        st.stop()

    date_col = st.sidebar.selectbox("Select Timeline Column", options=date_options, index=0)
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df = df.dropna(subset=[date_col]).sort_values(by=date_col)

    # 2. Target Selection
    numeric_cols = list(df.select_dtypes(include=[np.number]).columns)
    if not numeric_cols:
        st.error("No numerical columns found to analyze.")
        st.stop()

    target_col = st.sidebar.selectbox("Select Primary Target (Revenue/Sales)", options=numeric_cols, 
                                      index=len(numeric_cols)-1 if len(numeric_cols) > 1 else 0)

    # 3. Categorical Filters
    st.sidebar.markdown("---")
    st.sidebar.header("📊 Live Filters")
    categorical_cols = list(df.select_dtypes(include=['object', 'category', 'string']).columns)
    if date_col in categorical_cols: categorical_cols.remove(date_col)

    filtered_df = df.copy()
    for col in categorical_cols[:2]:
        unique_vals = ['All'] + list(df[col].dropna().unique())
        selected_val = st.sidebar.selectbox(f"Filter by {col}", unique_vals)
        if selected_val != 'All':
            filtered_df = filtered_df[filtered_df[col] == selected_val]

    # Data Engineering
    filtered_df['Engine_Month'] = filtered_df[date_col].dt.month
    for col in filtered_df.columns:
        if pd.api.types.is_numeric_dtype(filtered_df[col]):
            filtered_df[col] = filtered_df[col].fillna(0)
        else:
            filtered_df[col] = filtered_df[col].fillna("Unknown")

    # ==========================================
    # 📑 WORKSPACE TABS ARCHITECTURE
    # ==========================================
    tab_forecast, tab_leads, tab_summary = st.tabs([
        "📈 AI Sales Forecasting", 
        "🎯 Lead Scoring Matrix", 
        "💡 Executive Summary & Next Steps"
    ])

    # ------------------------------------------
    # TAB 1: AI FORECASTING (Existing Logic)
    # ------------------------------------------
    with tab_forecast:
        st.write("### 🔮 Predictive Analytics Model")
        model_choice = st.selectbox("Choose AI Algorithm", ["Gradient Boosting", "Random Forest", "Linear Regression"])
        
        ml_features_df = filtered_df.drop(columns=[date_col, target_col], errors='ignore')
        ml_encoded = pd.get_dummies(ml_features_df, drop_first=True)
        X = ml_encoded.select_dtypes(include=[np.number, bool])
        y = filtered_df[target_col]

        if len(X) > 5: 
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)
            model = GradientBoostingRegressor(random_state=42) if model_choice == "Gradient Boosting" else RandomForestRegressor(random_state=42) if model_choice == "Random Forest" else LinearRegression()
            
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)
            
            m_col1, m_col2 = st.columns(2)
            m_col1.metric("Model MAE", f"{mean_absolute_error(y_test, predictions):.2f}")
            m_col2.metric("Confidence (R-Squared)", f"{r2_score(y_test, predictions):.2f}")

            fig_forecast, ax_forecast = plt.subplots(figsize=(10, 3))
            ax_forecast.plot(range(len(y_test)), y_test.values, label='Actual', color='#0052cc', marker='o')
            ax_forecast.plot(range(len(predictions)), predictions, label='AI Forecast', color='#36b37e', linestyle='--', marker='x')
            ax_forecast.legend()
            st.pyplot(fig_forecast)
        else:
            st.warning("Not enough data to train the AI.")

    # ------------------------------------------
    # TAB 2: LEAD SCORING MATRIX
    # ------------------------------------------
    with tab_leads:
        st.write("### 🎯 Dynamic Lead Scoring Engine")
        st.markdown("Select an identifier (e.g., Neighborhood or Plan Level) and the metrics that dictate 'quality'. The engine will normalize these metrics into a 0-100 Lead Score.")
        
        if len(categorical_cols) > 0 and len(numeric_cols) > 0:
            l_col1, l_col2 = st.columns(2)
            with l_col1:
                entity_col = st.selectbox("Select Lead Identifier", categorical_cols)
            with l_col2:
                # Default to the target column if possible
                scoring_factors = st.multiselect("Select Scoring Factors (Metrics)", numeric_cols, default=[target_col])
            
            if scoring_factors:
                # Group data by the entity (e.g., total sales per neighborhood)
                lead_data = filtered_df.groupby(entity_col)[scoring_factors].sum().reset_index()
                
                # Normalize the data using Min-Max Scaler
                scaler = MinMaxScaler()
                scaled_data = scaler.fit_transform(lead_data[scoring_factors])
                
                # Calculate average score across selected factors and convert to 100-point scale
                lead_data['Lead_Score'] = scaled_data.mean(axis=1) * 100
                lead_data['Lead_Score'] = lead_data['Lead_Score'].round(1)
                
                # Sort and display
                top_leads = lead_data.sort_values(by='Lead_Score', ascending=False).reset_index(drop=True)
                st.dataframe(top_leads.style.background_gradient(subset=['Lead_Score'], cmap='Greens'), use_container_width=True)
            else:
                st.info("Select at least one metric to calculate lead scores.")
        else:
            st.info("Your dataset needs text categories and numeric values to score leads.")

    # ------------------------------------------
    # TAB 3: EXECUTIVE SUMMARY & TEXT RECOMMENDATIONS
    # ------------------------------------------
    with tab_summary:
        st.write("### 💡 Automated Executive Summary")
        
        # High-Level KPIs
        total_value = filtered_df[target_col].sum()
        avg_value = filtered_df[target_col].mean()
        max_value = filtered_df[target_col].max()
        
        k_col1, k_col2, k_col3 = st.columns(3)
        k_col1.metric(f"Total {target_col}", f"{total_value:,.2f}")
        k_col2.metric(f"Average {target_col}", f"{avg_value:,.2f}")
        k_col3.metric(f"Peak {target_col}", f"{max_value:,.2f}")
        
        st.markdown("---")
        st.write("### 📌 Strategic Next Steps")
        
        # Dynamic Text Engine
        if len(categorical_cols) > 0:
            top_category_col = categorical_cols[0]
            category_sums = filtered_df.groupby(top_category_col)[target_col].sum().sort_values(ascending=False)
            top_performer = category_sums.index[0]
            bottom_performer = category_sums.index[-1]
            
            st.success(f"**1. Capitalize on Top Performers:** The data indicates that **{top_performer}** is driving the highest overall {target_col}. Increase resource allocation and marketing spend in this segment for the next quarter.")
            st.warning(f"**2. Investigate Underperformers:** The **{bottom_performer}** segment is currently lagging. Initiate a brief audit to determine if this is a pricing issue, a drop in lead quality, or a seasonal trend.")
        
        st.info(f"**3. AI Model Refinement:** The AI forecasting engine is currently tracking {len(filtered_df)} data points. To improve the R-Squared confidence score, ingest additional historical data to capture deeper seasonal trends.")

else:
    st.info("🔌 Awaiting system payload connection. Upload a dataset in the sidebar to initiate the strategic intelligence modules.")