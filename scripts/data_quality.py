import os
from sqlalchemy import create_engine, text

def build_db_url():
    db_url = os.getenv("DB_URL")
    if db_url:
        return db_url

    host = os.getenv("DB_HOST")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    port = os.getenv("DB_PORT", "5433")
    dbname = os.getenv("DB_NAME", "olist_dw")

    if not host or not user or not password:
        raise RuntimeError(
            "Set DB_URL or DB_HOST/DB_USER/DB_PASSWORD environment variables."
        )

    return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

DB_URL = build_db_url()

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