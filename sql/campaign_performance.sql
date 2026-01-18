-- Campaign Performance Analysis
-- Calculating acceptance rates for each campaign

SELECT
    'Campaign 1' as campaign,
    SUM(AcceptedCmp1) as accepted_count,
    COUNT(*) as total,
    ROUND(
        CAST(SUM(AcceptedCmp1) as FLOAT) / COUNT(*) * 100,
        2
    ) as conversion_rate
FROM marketing_data
UNION ALL
SELECT 'Campaign 2', SUM(AcceptedCmp2), COUNT(*), ROUND(
        CAST(SUM(AcceptedCmp2) as FLOAT) / COUNT(*) * 100, 2
    )
FROM marketing_data
UNION ALL
SELECT 'Campaign 3', SUM(AcceptedCmp3), COUNT(*), ROUND(
        CAST(SUM(AcceptedCmp3) as FLOAT) / COUNT(*) * 100, 2
    )
FROM marketing_data
UNION ALL
SELECT 'Campaign 4', SUM(AcceptedCmp4), COUNT(*), ROUND(
        CAST(SUM(AcceptedCmp4) as FLOAT) / COUNT(*) * 100, 2
    )
FROM marketing_data
UNION ALL
SELECT 'Campaign 5', SUM(AcceptedCmp5), COUNT(*), ROUND(
        CAST(SUM(AcceptedCmp5) as FLOAT) / COUNT(*) * 100, 2
    )
FROM marketing_data
UNION ALL
SELECT 'Last Campaign', SUM(Response), COUNT(*), ROUND(
        CAST(SUM(Response) as FLOAT) / COUNT(*) * 100, 2
    )
FROM marketing_data;