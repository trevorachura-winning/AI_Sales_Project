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

st.set_page_config(page_title="AI+ Sales Forecasting", layout="wide")

st.title("📈 Sales Forecast using AI")
st.markdown("Upload your cleaned sales dataset to generate insights and AI predictions.")

# File Uploader
uploaded_file = st.file_uploader("Upload CSV File", type=['csv'])

if uploaded_file is not None:
    # Load Data
    df = pd.read_csv(uploaded_file)
    df['Date'] = pd.to_datetime(df['Date'])
    
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # Sidebar Filters
    st.sidebar.header("Filters")
    
    # Model Selection
    model_choice = st.sidebar.selectbox(
        "Select AI Model",
        ("Gradient Boosting", "Random Forest", "Linear Regression", "Decision Tree")
    )
    
    # Data Filters
    selected_region = st.sidebar.multiselect("Filter by Region", df['Region'].unique(), default=df['Region'].unique())
    selected_segment = st.sidebar.multiselect("Filter by Customer Segment", df['Customer_Segment'].unique(), default=df['Customer_Segment'].unique())
    selected_category = st.sidebar.multiselect("Filter by Product Category", df['Category'].unique(), default=df['Category'].unique())

    # Apply Filters
    filtered_df = df[
        (df['Region'].isin(selected_region)) & 
        (df['Customer_Segment'].isin(selected_segment)) &
        (df['Category'].isin(selected_category))
    ].copy()

    if filtered_df.empty:
        st.warning("No data available for the selected filters.")
    else:
        st.markdown("---")
        
        # Row 1: Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Average Sales: Weekday vs Weekend")
            # Creating a weekend flag (Saturday=5, Sunday=6)
            filtered_df['Is_Weekend'] = filtered_df['Date'].dt.dayofweek >= 5
            wknd_sales = filtered_df.groupby('Is_Weekend')['Units_Sold'].mean().rename(index={False: 'Weekday', True: 'Weekend'})
            fig, ax = plt.subplots()
            sns.barplot(x=wknd_sales.index, y=wknd_sales.values, ax=ax, palette="pastel")
            ax.set_ylabel("Average Units Sold")
            st.pyplot(fig)
            
        with col2:
            st.subheader("Average Sales by Promotion Type")
            promo_sales = filtered_df.groupby('Promotion_Type')['Units_Sold'].mean().reset_index()
            fig, ax = plt.subplots()
            sns.barplot(data=promo_sales, x='Promotion_Type', y='Units_Sold', ax=ax, palette="husl")
            ax.set_ylabel("Average Units Sold")
            st.pyplot(fig)

        # Row 2: Charts
        col3, col4 = st.columns(2)
        
        with col3:
            st.subheader("Total Units Sold by Product Category")
            cat_sales = filtered_df.groupby('Category')['Units_Sold'].sum().reset_index()
            fig, ax = plt.subplots()
            sns.barplot(data=cat_sales, x='Category', y='Units_Sold', ax=ax, palette="Set2")
            st.pyplot(fig)

        with col4:
            st.subheader("Product Category Share")
            fig, ax = plt.subplots()
            ax.pie(cat_sales['Units_Sold'], labels=cat_sales['Category'], autopct='%1.1f%%', colors=sns.color_palette("Set2"))
            st.pyplot(fig)

        st.markdown("---")
        st.header(f"🤖 AI Forecasting Model: {model_choice}")
        
        # Machine Learning Prep
        st.write("Training model on current filtered data...")
        
        # Prepare categorical features
        ml_df = pd.get_dummies(filtered_df, columns=['Category', 'Promotion_Type', 'Customer_Segment', 'Region'], drop_first=True)
        
        # Select numeric features for model
        features = [col for col in ml_df.columns if col not in ['Date', 'Product_ID', 'Units_Sold', 'Revenue', 'Competitor_Pricing_Indicator']]
        
       # Prepare data for AI (One-Hot Encoding)
        # Convert all useful text categories into 1s and 0s
        ml_df = pd.get_dummies(filtered_df, columns=['Category', 'Promotion_Type', 'Customer_Segment', 'Region', 'Day_of_Week'], drop_first=True)
        
        # BULLETPROOF FIX: Automatically drop ANY remaining text columns (like Product_ID) so the math model never crashes
        ml_df = ml_df.select_dtypes(exclude=['object', 'string'])
        
        # Drop target and non-predictive columns
        features = [col for col in ml_df.columns if col not in ['Date', 'Units_Sold', 'Revenue', 'Is_Weekend']]
        X = ml_df[features]
        y = filtered_df['Units_Sold'] # Pull target from original filtered data
        
        X = ml_df[features]
        y = ml_df['Units_Sold']
        
        if len(X) > 10: # Ensure enough data to train
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)
            
            # Model Selection Logic
            if model_choice == "Gradient Boosting":
                model = GradientBoostingRegressor(random_state=42)
            elif model_choice == "Random Forest":
                model = RandomForestRegressor(random_state=42)
            elif model_choice == "Linear Regression":
                model = LinearRegression()
            else:
                model = DecisionTreeRegressor(random_state=42)
                
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)
            
            mae = mean_absolute_error(y_test, predictions)
            r2 = r2_score(y_test, predictions)
            
            col_m1, col_m2 = st.columns(2)
            col_m1.metric("Mean Absolute Error (MAE)", f"{mae:.2f} units")
            col_m2.metric("R-Squared (Accuracy Score)", f"{r2:.2f}")
            
            st.subheader("Actual vs Predicted Sales")
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(range(len(y_test)), y_test.values, label='Actual Units Sold', color='orange')
            ax.plot(range(len(predictions)), predictions, label='Predicted Units Sold', linestyle='--', color='green')
            ax.set_xlabel("Sample Days (Test Set)")
            ax.set_ylabel("Units Sold")
            ax.legend()
            st.pyplot(fig)
            
            # Recommendations (Step 8)
            st.subheader("📌 Business Recommendations")
            st.info("""
            **Inventory Planning:** Use the predicted peaks to order stock proactively and avoid shortages.
            **Staffing:** Schedule additional staff during predicted high-demand periods (e.g., weekends/holidays).
            **Marketing:** Align your promotional spend with periods where the AI predicts a slump, or double down on high-performing promotion types identified in the charts above.
            """)
            
        else:
            st.error("Not enough data points after filtering to train the AI model. Please adjust your filters.")
else:
    st.info("Please upload your sales CSV file in the sidebar to begin.")