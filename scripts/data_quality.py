import os
from sqlalchemy import create_engine, text

DB_URL = os.getenv(
    "DB_URL",
    "postgresql://admin:admin@localhost:5433/olist_dw"
)

engine = create_engine(DB_URL)

checks = {
    "raw_orders_has_data": """
        SELECT CASE WHEN COUNT(*) > 0 THEN 0 ELSE 1 END
        FROM raw.orders
    """,

    "raw_order_items_has_data": """
        SELECT CASE WHEN COUNT(*) > 0 THEN 0 ELSE 1 END
        FROM raw.order_items
    """,

    "orders_null_order_id": """
        SELECT COUNT(*)
        FROM raw.orders
        WHERE order_id IS NULL
    """,

    "order_items_null_order_id": """
        SELECT COUNT(*)
        FROM raw.order_items
        WHERE order_id IS NULL
    """,

    "order_items_negative_price": """
        SELECT COUNT(*)
        FROM raw.order_items
        WHERE price < 0
    """,

    "order_items_negative_freight": """
        SELECT COUNT(*)
        FROM raw.order_items
        WHERE freight_value < 0
    """,

    "payments_negative_value": """
        SELECT COUNT(*)
        FROM raw.order_payments
        WHERE payment_value < 0
    """,

    "invalid_order_status": """
        SELECT COUNT(*)
        FROM raw.orders
        WHERE order_status NOT IN (
            'delivered',
            'shipped',
            'canceled',
            'unavailable',
            'invoiced',
            'processing',
            'created',
            'approved'
        )
    """,

    "warehouse_fact_has_data": """
        SELECT CASE WHEN COUNT(*) > 0 THEN 0 ELSE 1 END
        FROM warehouse.fact_order_items
    """
}

def run_checks():
    failed = False

    with engine.connect() as conn:
        for check_name, query in checks.items():
            result = conn.execute(text(query)).scalar()

            if result > 0:
                print(f"[FAILED] {check_name}: {result}")
                failed = True
            else:
                print(f"[PASSED] {check_name}")

    if failed:
        raise Exception("Data quality checks failed")

    print("All data quality checks passed.")

if __name__ == "__main__":
    run_checks()