<h1 align="center">🔥 Flame AI-Sales</h1>

<p align="center">
  <strong>Open-Source Enterprise Strategic Analytics & Intelligence Engine</strong><br>
  Transforming raw historical sales data into actionable, AI-driven foresight without writing a single line of code.
</p>

---

## 💡 Overview

Flame AI-Sales is an **open-source**, multi-page Streamlit application designed for business leaders and strategic planners. By combining machine learning algorithms with dynamic data engineering, the platform enables organizations to instantly ingest historical data, forecast future revenue, rank lead quality, and generate automated executive summaries. 

As an open-source initiative, this tool is designed to democratize enterprise-grade analytics, making powerful predictive models accessible to businesses of all sizes while welcoming community contributions.

## ✨ Key Features

* **🔒 Secure Gateway:** Protected access ensuring only authorized personnel can view organizational intelligence.
* **📂 Dynamic Data Ingestion:** Instantly maps uploaded `.csv` files into RAM, accommodating dynamic column structures and schemas.
* **📈 Predictive AI Forecasting:** Leverages multiple machine learning algorithms:
  * *Gradient Boosting* (High accuracy for complex cycles)
  * *Random Forest* (Prevents overfitting)
  * *Linear Regression* (For stable, predictable data)
* **🎯 Dynamic Lead Scoring:** Automatically normalizes selected categorical and numeric metrics to rank business leads on a 0-100 scale.
* **💡 Executive Summaries:** Generates natural language strategic next steps, identifying top-performing and under-performing segments.
* **🎛️ Live Filtering:** Slice and dice datasets on the fly by categories and timelines.

---

## 📋 Data Requirements

For the AI engine to successfully train and extract insights, uploaded datasets must meet the following criteria:
1. **Format:** Standard `.csv` file.
2. **Timeline:** Must contain at least one valid Date column (e.g., `YYYY-MM-DD`).
3. **Target Metric:** Must contain at least one purely numeric financial/sales column (no `$` or commas).
4. **Volume:** A minimum of 6 chronological data points (rows) is required to train the AI, though 20+ is highly recommended for confident R-Squared validation.
5. **Categorization:** Text-based columns (e.g., *Neighborhood, Acquisition Channel*) are required to utilize the Lead Scoring matrix.

---

## 🚀 Local Installation & Setup

To run this platform on your local machine, follow these steps:

**1. Clone the repository**
```bash
git clone [https://github.com/trevorachura-winning/Flame-AI-Sales.git](https://github.com/trevorachura-winning/Flame-AI-Sales.git)
cd Flame-AI-Sales