import streamlit as st
import pandas as pd
import sqlite3
import os
import plotly.express as px

# Set page config
st.set_page_config(page_title="Retail Pulse Analytics", layout="wide", page_icon="🏕️")

# Constants
DB_PATH = os.path.join(os.path.dirname(__file__), '../data/retail_pulse.db')
SQL_DIR = os.path.join(os.path.dirname(__file__), '../sql')

# Helper Functions
@st.cache_data
def run_query(query_file):
    """Executes a SQL query from a file and returns a DataFrame."""
    path = os.path.join(SQL_DIR, query_file)
    with open(path, 'r') as f:
        query = f.read()
    
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(query, conn)
        return df
    finally:
        conn.close()

# Whitelist of valid table names to prevent SQL injection
VALID_TABLES = {'customers', 'products', 'transactions', 'web_traffic', 'marketing_data'}

def load_data(table_name):
    """Loads a raw table from the database."""
    if table_name not in VALID_TABLES:
        raise ValueError(f"Invalid table name: {table_name}")
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df

# Main App Layout
st.title("🏕️ Retail Pulse: Analytics Dashboard")
st.markdown("Monitor sales performance, customer segments, and web traffic conversion.")


# Sidebar Navigation
page = st.sidebar.radio("Navigate", ["Executive Summary", "Customer Segmentation", "Marketing Campaigns", "Data View"])

# --- PAGE 1: EXECUTIVE SUMMARY ---
if page == "Executive Summary":
    st.header("📊 Customer Profile Overview")
    
    # Load Data (Summary stats from SQL or direct DB)
    conn = sqlite3.connect(DB_PATH)
    summary_df = pd.read_sql_query("SELECT COUNT(*) as customers, AVG(Income) as avg_income, SUM(MntWines + MntFruits + MntMeatProducts + MntFishProducts + MntSweetProducts + MntGoldProds) as total_spend FROM marketing_data", conn)
    conn.close()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Customers", f"{summary_df['customers'][0]:,}")
    col2.metric("Avg Household Income", f"${summary_df['avg_income'][0]:,.0f}")
    col3.metric("Total Lifetime Spend", f"${summary_df['total_spend'][0]:,.0f}")
    
    st.markdown("---")
    
    # Spend by Category
    conn = sqlite3.connect(DB_PATH)
    spend_df = pd.read_sql_query("""
        SELECT 
            SUM(MntWines) as Wines, 
            SUM(MntFruits) as Fruits, 
            SUM(MntMeatProducts) as Meat, 
            SUM(MntFishProducts) as Fish, 
            SUM(MntSweetProducts) as Sweets, 
            SUM(MntGoldProds) as Gold 
        FROM marketing_data
    """, conn)
    conn.close()
    
    spend_melted = spend_df.melt(var_name='Category', value_name='TotalSales')
    
    st.subheader("🛒 Spend Distribution by Category")
    fig_bar = px.bar(spend_melted, x='Category', y='TotalSales', color='Category', title="Which Products Drive Revenue?")
    st.plotly_chart(fig_bar, width='stretch', key="spend_by_category_bar")

# --- PAGE 2: CUSTOMER SEGMENTATION ---
elif page == "Customer Segmentation":
    st.header("👥 Value Segments & Demographics")
    
    # Load Data
    rfm_df = run_query('rfm_analysis.sql')
    
    # Scatter Plot: Income vs Spend
    st.subheader("Income vs. Total Spend")
    fig_scatter = px.scatter(
        rfm_df, 
        x='Income', 
        y='monetary_value', 
        color='Education',
        size='frequency',
        hover_data=['Marital_Status', 'Year_Birth'],
        title="Who are our High-Value Customers?",
        labels={'monetary_value': 'Total Spend ($)', 'Income': 'Annual Income ($)'}
    )
    # Filter outliers for better visualization on default view
    fig_scatter.update_xaxes(range=[0, 200000]) 
    st.plotly_chart(fig_scatter, width='stretch', key="income_vs_spend_scatter")
    
    # Demographics Analysis
    st.subheader("🎓 Education & Marital Status Analysis")
    demo_df = run_query('demographics.sql')
    
    fig_demo = px.bar(
        demo_df, 
        x='Education', 
        y='avg_total_spend', 
        color='Marital_Status', 
        barmode='group',
        title="Average Spend by Education & Status"
    )
    st.plotly_chart(fig_demo, width='stretch', key="demographics_bar")

# --- PAGE 3: MARKETING CAMPAIGNS ---
elif page == "Marketing Campaigns":
    st.header("📢 Campaign Performance")
    
    # Load Data
    camp_df = run_query('campaign_performance.sql')
    
    st.subheader("Campaign Conversion Rates")
    st.info("Conversion Rate = Percentage of customers who accepted the offer.")
    
    fig_funnel = px.bar(
        camp_df, 
        x='campaign', 
        y='conversion_rate', 
        color='conversion_rate',
        text='conversion_rate',
        title="Success Rate by Campaign",
        labels={'conversion_rate': 'Conversion Rate (%)'}
    )
    fig_funnel.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    st.plotly_chart(fig_funnel, width='stretch', key="campaign_conversion_bar")
    
    # Deep dive into the Last Campaign (Response)
    st.subheader("Profile of 'Last Campaign' Responders")
    
    conn = sqlite3.connect(DB_PATH)
    # Compare income of responders vs non-responders
    resp_df = pd.read_sql_query("SELECT Response, Income, (MntWines+MntMeatProducts+MntGoldProds+MntFishProducts+MntFruits+MntSweetProducts) as TotalSpend FROM marketing_data", conn)
    conn.close()
    
    resp_df['Status'] = resp_df['Response'].apply(lambda x: 'Accepted' if x == 1 else 'Rejected')
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_box1 = px.box(resp_df, x='Status', y='Income', title="Income Distribution")
        fig_box1.update_yaxes(range=[0, 200000])
        st.plotly_chart(fig_box1, width='stretch', key="income_boxplot")
        
    with col2:
        fig_box2 = px.box(resp_df, x='Status', y='TotalSpend', title="Total Spend Distribution")
        st.plotly_chart(fig_box2, width='stretch', key="spend_boxplot")

# --- PAGE 4: DATA VIEW ---
elif page == "Data View":
    st.header("💾 Raw Data Inspector")
    st.dataframe(load_data('marketing_data'))


st.sidebar.markdown("---")
st.sidebar.caption("Retail Pulse Portfolio Project")
