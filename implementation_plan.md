# Implementation Plan: Marketing Campaign Analysis

**Objective**: Refactor Retail Pulse to use the `marketing_campaign.csv` dataset. This shifts the focus from transactional sales analysis to **Customer Profiling & Campaign Performance**.

## Phase 1: Database Refactoring
1.  **Modify `src/db_manager.py`**:
    -   Update `init_db` to create a new table `marketing_data` matching the CSV columns.
    -   Update `clean_and_load` to read `marketing_campaign.csv` (Tab-separated).
    -   Clean: Handle missing values in `Income`. Parse `Dt_Customer` to date format.

## Phase 2: Analysis Layer (SQL Updates)
2.  **Update SQL Scripts**:
    -   `rfm_analysis.sql`: Map existing RFM concepts to the new dataset columns.
        -   **Recency**: `Recency` (days since purchase).
        -   **Frequency**: Sum of `NumWebPurchases`, `NumCatalogPurchases`, `NumStorePurchases`.
        -   **Monetary**: Sum of `MntWines`, `MntMeatProducts`, `MntFishProducts`, `MntSweetProducts`, `MntGoldProds`, `MntFruits`.
    -   **[NEW]** `demographics.sql`: Group by `Education`, `Marital_Status` and avg `Income`.
    -   **[NEW]** `campaign_performance.sql`: Acceptance rates for Cmp1, Cmp2, Cmp3, Cmp4, Cmp5.

## Phase 3: Dashboard Overhaul
3.  **Update `src/app.py`**:
    -   **Executive Summary**:
        -   Metrics: Total Customers, Average Income, Total Spend.
        -   Chart: Spend by Category (Bar chart of MntWines vs MntGold etc).
    -   **Customer Segments**:
        -   Keep RFM Scatter plot (adapted to new query).
        -   Add Demographics charts (Education distribution).
    -   **Campaign Analysis** (New Page):
        -   Visualize acceptance rates of different campaigns.
        -   Compare "Responders" vs "Non-Responders".
