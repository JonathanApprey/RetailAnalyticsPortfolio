# Task Checklist for Code Claude

Please execute the following tasks in order. Check them off as you go.

## Environment & Setup
- [x] Create folder structure (`src`, `data`, `sql`).
- [x] Create `requirements.txt` with: `pandas`, `numpy`, `faker`, `streamlit`, `plotly`, `matplotlib`.
- [x] Install dependencies: `pip install -r requirements.txt`.

## Data EngineeringModule
- [x] **Implement Data Generator**:
    - [x] Create `src/data_generator.py`.
    - [x] Function `generate_customers(n=100)` returning a DataFrame.
    - [x] Function `generate_products()` returns DataFrame of camping/RV result items.
    - [x] Function `generate_transactions(n=500)` linking customers and products.
    - [x] Main block to save these as CSVs to `data/raw/` (create dir first).
- [x] **Implement Database Manager**:
    - [x] Create `src/db_manager.py`.
    - [x] Write `init_db()` to create SQLite tables: `customers`, `products`, `transactions`.
    - [x] Write `clean_and_load()`: Read CSVs, drop duplicates, load to SQLite.
- [x] **Execution**: Run the generator and loader to populate `retail_pulse.db`.

## Analytical Queries
- [x] Create `sql/kpi_sales.sql`: Query for total revenue and order count per month.
- [x] Create `sql/rfm_analysis.sql`: Query calculating Recency, Frequency, Monetary value per customer.
- [x] Verify queries by running them against the DB in a separate test script or terminal.

## Dashboard Development
- [x] **Setup App**: Create `src/app.py` with basic Streamlit layout.
- [x] **Data Connection**: Add function in `app.py` to connect to SQLite and run queries.
- [x] **Dashboard - Page 1**: Implement "Overview" tab with Sales Trend line chart.
- [x] **Dashboard - Page 2**: Implement "Customer Segments" tab with RFM scatter plot.
- [x] **Dashboard - Page 3**: Implement "Data View" tab showing raw tables for inspection.

## Final Polish
- [x] Add comments to all code explaining *why* (e.g., "Cleaning nulls to ensure accurate averages").
- [x] Create `README.md` explaining how to run the project.
