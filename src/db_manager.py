import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../data/retail_pulse.db')
RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), '../data/raw')

def init_db():
    """
    Initializes the SQLite database with the required tables.
    """
    print(f"Initializing database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create Tables for original synthetic data (keeping for reference unless fully replaced)
    cursor.execute('''CREATE TABLE IF NOT EXISTS customers (customer_id INTEGER PRIMARY KEY, name TEXT, email TEXT, state TEXT, signup_date DATE)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (product_id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (order_id INTEGER PRIMARY KEY, customer_id INTEGER, product_id INTEGER, date DATE, amount REAL, quantity INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS web_traffic (session_id TEXT, user_id INTEGER, page_path TEXT, duration_seconds INTEGER, converted BOOLEAN, timestamp DATETIME)''')

    # --- NEW: Marketing Campaign Table ---
    # Based on the CSV structure: ID, Year_Birth, Education, Marital_Status, Income, etc.
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS marketing_data (
        ID INTEGER PRIMARY KEY,
        Year_Birth INTEGER,
        Education TEXT,
        Marital_Status TEXT,
        Income REAL,
        Kidhome INTEGER,
        Teenhome INTEGER,
        Dt_Customer DATE,
        Recency INTEGER,
        MntWines REAL,
        MntFruits REAL,
        MntMeatProducts REAL,
        MntFishProducts REAL,
        MntSweetProducts REAL,
        MntGoldProds REAL,
        NumDealsPurchases INTEGER,
        NumWebPurchases INTEGER,
        NumCatalogPurchases INTEGER,
        NumStorePurchases INTEGER,
        NumWebVisitsMonth INTEGER,
        AcceptedCmp3 INTEGER,
        AcceptedCmp4 INTEGER,
        AcceptedCmp5 INTEGER,
        AcceptedCmp1 INTEGER,
        AcceptedCmp2 INTEGER,
        Complain INTEGER,
        Z_CostContact INTEGER,
        Z_Revenue INTEGER,
        Response INTEGER
    )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized.")

def clean_and_load():
    """
    Reads CSVs, cleans data, and loads it into the database.
    """
    print("Loading data...")
    conn = sqlite3.connect(DB_PATH)
    
    # --- Load Marketing Campaign Data ---
    marketing_path = os.path.join(os.path.dirname(__file__), '../marketing_campaign.csv')
    if os.path.exists(marketing_path):
        print(f"Loading {marketing_path}...")
        # Read Tab-Separated Values (sep='\t')
        df = pd.read_csv(marketing_path, sep='\t')
        
        # Data Cleaning
        # 1. Handle missing Income (fill with median)
        df['Income'] = df['Income'].fillna(df['Income'].median())
        
        # 2. Parse Dt_Customer to YYYY-MM-DD
        # Original format seems to be dd-mm-yyyy based on view_file output (e.g. 04-09-2012)
        df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'], dayfirst=True).dt.date
        
        # 3. Clean Marital Status (consolidate 'Alone', 'Absurd', 'YOLO' -> 'Single' or similar if needed, keeping simple for now)
        
        df.to_sql('marketing_data', conn, if_exists='replace', index=False)
        print("Marketing data loaded.")
    else:
        print("Warning: marketing_campaign.csv not found at expected path.")
    
    conn.close()
    print("Data loaded successfully.")

if __name__ == "__main__":
    init_db()
    clean_and_load()
