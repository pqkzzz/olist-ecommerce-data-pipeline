SELECT
    p.product_id,

    COALESCE(
        t.product_category_name_english,
        p.product_category_name,
        'unknown'
    ) AS product_category_name,

    p.product_name_lenght::int AS product_name_length,
    p.product_description_lenght::int AS product_description_length,
    p.product_photos_qty::int AS product_photos_qty,
    p.product_weight_g::numeric AS product_weight_g,
    p.product_length_cm::numeric AS product_length_cm,
    p.product_height_cm::numeric AS product_height_cm,
    p.product_width_cm::numeric AS product_width_cm

FROM {{ source('raw', 'products') }} p
LEFT JOIN {{ source('raw', 'product_category_translation') }} t
    ON p.product_category_name = t.product_category_name