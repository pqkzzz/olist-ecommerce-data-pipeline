SELECT
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix,
    LOWER(customer_city) AS customer_city,
    UPPER(customer_state) AS customer_state
FROM {{ source('raw', 'customers') }}