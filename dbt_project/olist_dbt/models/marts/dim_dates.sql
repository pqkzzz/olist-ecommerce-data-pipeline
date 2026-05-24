WITH dates AS (
    SELECT DISTINCT
        order_purchase_timestamp::date AS full_date
    FROM {{ ref('stg_orders') }}
    WHERE order_purchase_timestamp IS NOT NULL
)

SELECT
    TO_CHAR(full_date, 'YYYYMMDD')::int AS date_id,
    full_date,
    EXTRACT(day FROM full_date)::int AS day,
    EXTRACT(month FROM full_date)::int AS month,
    EXTRACT(quarter FROM full_date)::int AS quarter,
    EXTRACT(year FROM full_date)::int AS year,
    EXTRACT(dow FROM full_date)::int AS day_of_week
FROM dates