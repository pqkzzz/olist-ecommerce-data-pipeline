SELECT
    seller_id,
    seller_zip_code_prefix,
    LOWER(seller_city) AS seller_city,
    UPPER(seller_state) AS seller_state
FROM raw.sellers