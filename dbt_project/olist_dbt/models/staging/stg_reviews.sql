SELECT
    review_id,
    order_id,
    review_score,
    review_creation_date::timestamp AS review_creation_date,
    review_answer_timestamp::timestamp AS review_answer_timestamp
FROM {{ source('raw', 'order_reviews') }}