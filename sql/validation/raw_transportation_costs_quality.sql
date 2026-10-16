-- OpsIntel BI
-- Raw transportation-cost data-quality validation

-- 1. Total rows
SELECT
    COUNT(*) AS transportation_cost_rows
FROM raw.transportation_costs;

-- 2. Duplicate transportation cost IDs
SELECT
    transportation_cost_id,
    COUNT(*) AS row_count
FROM raw.transportation_costs
GROUP BY transportation_cost_id
HAVING COUNT(*) > 1
ORDER BY row_count DESC, transportation_cost_id;

-- 3. Missing shipment references
SELECT
    COUNT(*) AS missing_shipment_reference
FROM raw.transportation_costs
WHERE shipment_id IS NULL;

-- 4. Cost distribution
SELECT
    MIN(cost_amount) AS min_cost,
    MAX(cost_amount) AS max_cost,
    AVG(cost_amount) AS avg_cost,
    PERCENTILE_CONT(0.50)
        WITHIN GROUP (ORDER BY cost_amount) AS median_cost,
    PERCENTILE_CONT(0.95)
        WITHIN GROUP (ORDER BY cost_amount) AS p95_cost,
    PERCENTILE_CONT(0.99)
        WITHIN GROUP (ORDER BY cost_amount) AS p99_cost
FROM raw.transportation_costs;

-- 5. Negative cost records
SELECT
    transaction_type,
    cost_type,
    COUNT(*) AS row_count,
    SUM(cost_amount) AS total_amount
FROM raw.transportation_costs
WHERE cost_amount < 0
GROUP BY transaction_type, cost_type
ORDER BY row_count DESC;

-- 6. Positive credits or reversals
SELECT
    COUNT(*) AS invalid_credit_sign_rows
FROM raw.transportation_costs
WHERE transaction_type IN ('CREDIT', 'REVERSAL')
  AND cost_amount > 0;

-- 7. Cost types
SELECT
    cost_type,
    COUNT(*) AS row_count,
    ROUND(AVG(cost_amount), 2) AS average_cost
FROM raw.transportation_costs
GROUP BY cost_type
ORDER BY row_count DESC;

-- 8. Transaction types
SELECT
    transaction_type,
    COUNT(*) AS row_count
FROM raw.transportation_costs
GROUP BY transaction_type
ORDER BY row_count DESC;