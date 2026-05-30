SELECT
    CONCAT(order_id, '-', payment_sequential) AS payment_key,
    order_id,
    payment_sequential,
    payment_type,
    payment_installments,
    payment_value

FROM {{ ref('stg_payments') }}