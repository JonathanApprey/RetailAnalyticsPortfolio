-- RFM Analysis adapted for marketing_data
-- Recency: Directly available as 'Recency' column (days since purchase)
-- Frequency: Sum of all purchase counts (Web, Catalog, Store)
-- Monetary: Sum of all spending amounts (Wines, Fruits, Meat, Fish, Sweet, Gold)

SELECT
    ID as customer_id,
    Year_Birth,
    Education,
    Marital_Status,
    Income,
    Recency as recency_days,
    (
        NumWebPurchases + NumCatalogPurchases + NumStorePurchases
    ) as frequency,
    (
        MntWines + MntFruits + MntMeatProducts + MntFishProducts + MntSweetProducts + MntGoldProds
    ) as monetary_value,
    Response as responded_last_campaign
FROM marketing_data
WHERE
    Income IS NOT NULL
ORDER BY monetary_value DESC;