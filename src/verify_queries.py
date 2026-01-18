import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../data/retail_pulse.db')
SQL_DIR = os.path.join(os.path.dirname(__file__), '../sql')

def run_query(filename):
    print(f"\n--- Running {filename} ---")
    with open(os.path.join(SQL_DIR, filename), 'r') as f:
        query = f.read()
    
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(query, conn)
        print(df.head())
        print(f"Returned {len(df)} rows.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    run_query('kpi_sales.sql')
    run_query('rfm_analysis.sql')
    run_query('demographics.sql')
    run_query('campaign_performance.sql')
