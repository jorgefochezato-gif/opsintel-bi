-- OpsIntel BI
-- Staging transportation-cost validation

-- 1. Total staged cost records
SELECT
    COUNT(*) AS staging_transportation_cost_rows
FROM staging.transportation_costs_clean;

-- 2. Transportation cost IDs must be unique
SELECT
    COUNT(*) AS duplicate_transportation_cost_ids
FROM (
    SELECT transportation_cost_id
    FROM staging.transportation_costs_clean
    GROUP BY transportation_cost_id
    HAVING COUNT(*) > 1
) duplicates;

-- 3. Quality status distribution
SELECT
    quality_status,
    COUNT(*) AS row_count
FROM staging.transportation_costs_clean
GROUP BY quality_status
ORDER BY quality_status;

-- 4. Quality warning reasons
SELECT
    quality_notes,
    COUNT(*) AS row_count
FROM staging.transportation_costs_clean
WHERE quality_status = 'WARNING'
GROUP BY quality_notes
ORDER BY row_count DESC;

-- 5. Credit / reversal sign check
SELECT
    COUNT(*) AS positive_credit_or_reversal_rows
FROM staging.transportation_costs_clean
WHERE transaction_type IN ('CREDIT', 'REVERSAL')
  AND cost_amount > 0;

-- 6. Cost distribution
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
FROM staging.transportation_costs_clean;