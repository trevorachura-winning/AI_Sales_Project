# 📈 AI+ Sales Forecasting Dashboard

A hands-on machine learning web application built as part of the **AI+ Sales Labs™ (AICERTS™)** program. This interactive dashboard empowers business stakeholders to upload past transactional data, clean it on the fly, analyze overall retail trends, and train machine learning models to forecast future sales volume dynamically.

🔗 **Live Deployment Link:** https://aisalesproject-7vyut77gtpul3qbajgmxbf.streamlit.app/
🔗 **Repository URL:** https://github.com/trevorachura-winning/AI_Sales_Project

---

## 🚀 Project Overview
Accurate sales forecasting is critical for optimizing inventory levels, planning promotional calendars, and preventing stockouts. This project implements a full end-to-end data pipeline to solve this challenge. 

Instead of treating AI as a static "black box," this platform allows users to explore data patterns via descriptive analytics, toggle between multiple predictive algorithms, and view live performance metrics alongside actionable, automated business recommendations.

---

## 📊 Key Features
- **Dynamic File Ingestion:** Drag-and-drop support for any standardized past transactional CSV record format.
- **Granular Multi-Filters:** Drill down into forecasting insights instantly by filtering the incoming data by *Region*, *Customer Segment*, or *Product Category*.
- **Interactive Machine Learning:** Select and compare four distinct core regression algorithms directly from the sidebar.
- **Descriptive Analytics Visualizations:**
  - Average sales compared across weekdays vs. weekends.
  - Performance comparisons across various historical promotion models.
  - Aggregated market volume charts and proportional market share distribution maps.
- **Heuristic-Driven Recommendations:** Live automated guidance suggesting inventory buffer levels and strategic promotional planning based on the filtered analytics curves.

---

## 🗃️ Dataset Structure
The platform leverages a highly granular, 1.5-year daily synthetic dataset containing over 15 rich economic and behavioral features:
- **Temporal Attributes:** `Date`, `Day_of_Week`, `Month`, `Quarter`, `Holiday_Indicator`
- **Product Architecture:** `Product_ID`, `Category`, `Price`
- **Operational Metrics:** `Inventory_Levels`, `Competitor_Pricing_Indicator`
- **Customer Segmentation:** `Customer_Segment`, `Region`
- **Target Sales Variables:** `Units_Sold`, `Revenue`, `Discount_Applied`, `Promotion_Type`

---

## 🤖 Machine Learning Implementation
The backend pipeline processes and trains model data using the following programmatic architecture:
1. **Data Preprocessing & Cleaning:** Standardizes date strings, identifies and purges structural data duplicates, and guarantees continuous timeline continuity by filling skipped calendar gaps with `0` values.
2. **One-Hot Encoding:** Programmatically vectorizes string-based categoricals (`Category`, `Promotion_Type`, `Region`, `Day_of_Week`) using dummy bit flags (`pd.get_dummies`) to translate categorical dimensions into numerical tensors for the models.
3. **Data Segregation:** Splitting matrices via an 80/20 sequential layout (`train_test_split`) ensuring validation calculations happen against chronological unseen timelines.
4. **Predictive Analytics Engines:**
   - **Gradient Boosting Regressor** (Ensemble tree booster optimized for low error margins)
   - **Random Forest Regressor** (Bagging method optimized to avoid overfitting)
   - **Decision Tree Regressor** (Non-linear branching tree)
   - **Linear Regression** (Parametric baseline mapping linear trends)
5. **Model Evaluation:** Real-time generation of **Mean Absolute Error (MAE)** to gauge target variation and **R-Squared ($R^2$)** to score relative directional accuracy.

---

## 🛠️ Technologies & Libraries Used
- **Language:** Python
- **Interface & Deployment:** Streamlit Community Cloud
- **Data Engineering:** Pandas, NumPy
- **Data Visualization:** Matplotlib, Seaborn
- **Machine Learning Algorithms:** Scikit-Learn

---

## 💻 Local Setup & Execution Guide

If you wish to test, build, or run this interactive dashboard interface on your local workstation, execute the following configuration:

### Prerequisites
Ensure you have Python 3.10+ and Git installed on your device.

### 1. Clone the Workspace
```bash
git clone [https://github.com/your-username/AI_Sales_Project.git](https://github.com/your-username/AI_Sales_Project.git)
cd AI_Sales_Project
