# 🏕️ Retail Pulse: Portfolio Project

**Retail Pulse** is an end-to-end data analytics project simulating a retail environment (Camping & RV Gear). It demonstrates the full data lifecycle: generating synthetic data, building an ETL pipeline with SQLite, running SQL analysis, and visualizing KPIs in an interactive Streamlit dashboard.

## 🚀 Features

-   **Data Engineering**: 
    -   Synthetic data generation using `Faker` (Customers, Products, Transactions, Web Traffic).
    -   ETL pipeline to clean and load data into a SQLite database.
-   **SQL Analysis**: 
    -   Complex queries for RFM (Recency, Frequency, Monetary) segmentation.
    -   Monthly sales aggregations and web conversion funnels.
-   **Interactive Dashboard**: 
    -   Built with **Streamlit** and **Plotly**.
    -   Visualizes Sales Trends, Customer Segments, and Web Traffic.

## 🛠️ Tech Stack

-   **Python 3.9+**
-   **Pandas & NumPy**: Data manipulation.
-   **SQLite**: Relational database.
-   **Streamlit**: Web application framework.
-   **Plotly**: Interactive visualizations.

## 🏁 Getting Started

### 1. Installation

Clone the repository and install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Data Generation & Setup

Run the following command to generate synthetic data and populate the database:

```bash
# Generate CSVs and Load into SQLite
python3 src/data_generator.py
python3 src/db_manager.py
```

### 3. Run the Dashboard

Launch the Streamlit app:

```bash
streamlit run src/app.py
```

The app will open in your browser at `http://localhost:8501`.

## 📂 Project Structure

```
RetailPulse/
├── src/
│   ├── data_generator.py  # Generates synthetic data
│   ├── db_manager.py      # ETL: Loads CSVs to SQLite
│   └── app.py             # Streamlit Dashboard Entry Point
├── data/
│   ├── raw/               # Generated CSV files
│   └── retail_pulse.db    # SQLite Database
├── sql/                   # SQL Scripts for Analysis
│   ├── kpi_sales.sql
│   └── rfm_analysis.sql
└── requirements.txt
```
