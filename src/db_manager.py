import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../data/retail_pulse.db')

def init_db():
    """
    Initializes the SQLite database with the required tables.
    """
    print(f"Initializing database at {DB_PATH}...")
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Marketing Campaign Table
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
    Reads marketing_campaign.csv, cleans data, and loads it into the database.
    """
    print("Loading data...")
    conn = sqlite3.connect(DB_PATH)
    
    marketing_path = os.path.join(os.path.dirname(__file__), '../marketing_campaign.csv')
    if os.path.exists(marketing_path):
        print(f"Loading {marketing_path}...")
        # Read Tab-Separated Values
        df = pd.read_csv(marketing_path, sep='\t')
        
        # Data Cleaning
        # 1. Handle missing Income (fill with median)
        df['Income'] = df['Income'].fillna(df['Income'].median())
        
        # 2. Parse Dt_Customer to YYYY-MM-DD
        df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'], dayfirst=True).dt.date
        
        # 3. Clean unusual Marital Status values
        df['Marital_Status'] = df['Marital_Status'].replace({
            'Alone': 'Single',
            'Absurd': 'Other',
            'YOLO': 'Other'
        })
        
        df.to_sql('marketing_data', conn, if_exists='replace', index=False)
        print(f"Loaded {len(df)} records.")
    else:
        print("Error: marketing_campaign.csv not found.")
    
    conn.close()
    print("Data loaded successfully.")

if __name__ == "__main__":
    init_db()
    clean_and_load()
