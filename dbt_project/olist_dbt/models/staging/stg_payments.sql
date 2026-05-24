SELECT
    order_id,
    payment_sequential,
    payment_type,
    payment_installments,
    payment_value::numeric AS payment_value
FROM raw.order_payments