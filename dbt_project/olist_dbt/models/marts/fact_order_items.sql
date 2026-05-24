SELECT
    oi.order_id,
    oi.order_item_id,

    o.customer_id,
    oi.product_id,
    oi.seller_id,

    TO_CHAR(o.order_purchase_timestamp::date, 'YYYYMMDD')::int AS order_date_id,
    o.order_purchase_timestamp,
    o.order_status,

    oi.price,
    oi.freight_value,
    oi.price + oi.freight_value AS total_order_item_value,

    o.order_estimated_delivery_date,
    o.order_delivered_customer_date,

    CASE
        WHEN o.order_delivered_customer_date IS NULL THEN NULL
        WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 1
        ELSE 0
    END AS is_late_delivery,

    CASE
        WHEN o.order_delivered_customer_date IS NULL THEN NULL
        ELSE EXTRACT(day FROM o.order_delivered_customer_date - o.order_purchase_timestamp)
    END AS delivery_days

FROM {{ ref('stg_order_items') }} oi
LEFT JOIN {{ ref('stg_orders') }} o
    ON oi.order_id = o.order_id