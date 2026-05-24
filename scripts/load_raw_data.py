import os
import pandas as pd
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

RAW_DATA_PATH = "data/raw"

engine = create_engine(DB_URL)

csv_tables = {
    "olist_customers_dataset.csv": "customers",
    "olist_geolocation_dataset.csv": "geolocation",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_orders_dataset.csv": "orders",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "product_category_name_translation.csv": "product_category_translation",
}

def create_schema():
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
        conn.commit()

def load_csv(file_name, table_name):
    file_path = os.path.join(RAW_DATA_PATH, file_name)

    print(f"Loading {file_name} into raw.{table_name}...")

    df = pd.read_csv(file_path)

    df.to_sql(
        name=table_name,
        con=engine,
        schema="raw",
        if_exists="replace",
        index=False
    )

    print(f"Loaded {len(df)} rows into raw.{table_name}")

def main():
    create_schema()

    for file_name, table_name in csv_tables.items():
        load_csv(file_name, table_name)

    print("All raw data loaded successfully.")

if __name__ == "__main__":
    main()