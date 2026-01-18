-- Demographics Analysis
-- Grouping by Education and Marital Status to see spending power

SELECT
    Education,
    Marital_Status,
    COUNT(ID) as customer_count,
    ROUND(AVG(Income), 2) as avg_income,
    ROUND(
        AVG(
            MntWines + MntFruits + MntMeatProducts + MntFishProducts + MntSweetProducts + MntGoldProds
        ),
        2
    ) as avg_total_spend
FROM marketing_data
WHERE
    Income IS NOT NULL
GROUP BY
    1,
    2
HAVING
    customer_count > 5 -- Filter out rare categories like "YOLO" if distinct
ORDER BY avg_total_spend DESC;