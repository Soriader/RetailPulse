from __future__ import annotations

import random
from datetime import datetime, timedelta

import pandas as pd
from sqlalchemy import text

from retailpulse.db import get_engine


def _random_datetime(start: datetime, end: datetime) -> datetime:
    delta = end - start
    seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=seconds)


def generate_users(n_users: int = 1000) -> pd.DataFrame:
    countries = ["PL", "DE", "CZ", "SK", "UK"]
    cities_pl = ["Warszawa", "Gdańsk", "Poznań", "Wrocław", "Kraków", "Katowice"]
    cities_other = ["Berlin", "Prague", "Bratislava", "London"]

    now = datetime.now()
    start = now - timedelta(days=365)

    rows = []
    for user_id in range(1, n_users + 1):
        country = random.choice(countries)
        city = random.choice(cities_pl if country == "PL" else cities_other)
        created_at = _random_datetime(start, now)
        rows.append((user_id, created_at, country, city))

    return pd.DataFrame(rows, columns=["user_id", "created_at", "country", "city"])


def generate_products(n_products: int = 200) -> pd.DataFrame:
    categories = ["Kawa", "Herbata", "Akcesoria", "Słodycze", "Sprzęt"]
    rows = []
    for product_id in range(1, n_products + 1):
        category = random.choice(categories)
        product_name = f"{category} #{product_id}"
        price = round(random.uniform(9.99, 399.99), 2)
        rows.append((product_id, category, product_name, price))

    return pd.DataFrame(rows, columns=["product_id", "category", "product_name", "price"])


def generate_orders(users: pd.DataFrame, n_orders: int = 5000) -> pd.DataFrame:
    payment_methods = ["card", "blik", "transfer"]
    statuses = ["completed", "cancelled", "refunded"]

    now = datetime.now()
    start = now - timedelta(days=180)

    user_ids = users["user_id"].tolist()
    rows = []
    for order_id in range(1, n_orders + 1):
        user_id = random.choice(user_ids)
        order_datetime = _random_datetime(start, now)
        payment_method = random.choice(payment_methods)
        status = random.choices(statuses, weights=[0.88, 0.08, 0.04], k=1)[0]
        rows.append((order_id, user_id, order_datetime, payment_method, status))

    return pd.DataFrame(
        rows,
        columns=["order_id", "user_id", "order_datetime", "payment_method", "status"],
    )


def generate_order_items(orders: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    product_ids = products["product_id"].tolist()
    price_by_product = dict(zip(products["product_id"], products["price"]))

    rows = []
    for order_id in orders["order_id"].tolist():
        items_count = random.randint(1, 5)
        chosen_products = random.sample(product_ids, k=items_count)

        for product_id in chosen_products:
            qty = random.randint(1, 4)
            unit_price = float(price_by_product[product_id])
            rows.append((order_id, product_id, qty, unit_price))

    return pd.DataFrame(rows, columns=["order_id", "product_id", "qty", "unit_price"])


def truncate_raw_tables(engine):
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM raw_order_items;"))
        conn.execute(text("DELETE FROM raw_orders;"))
        conn.execute(text("DELETE FROM raw_products;"))
        conn.execute(text("DELETE FROM raw_users;"))


def load_raw(engine, users: pd.DataFrame, products: pd.DataFrame, orders: pd.DataFrame, items: pd.DataFrame):
    users.to_sql("raw_users", con=engine, if_exists="append", index=False)
    products.to_sql("raw_products", con=engine, if_exists="append", index=False)
    orders.to_sql("raw_orders", con=engine, if_exists="append", index=False)
    items.to_sql("raw_order_items", con=engine, if_exists="append", index=False)


def main():
    engine = get_engine()

    print("Generating data...")
    users = generate_users(1000)
    products = generate_products(200)
    orders = generate_orders(users, 5000)
    items = generate_order_items(orders, products)

    print("Users:", len(users), "Products:", len(products), "Orders:", len(orders), "Order items:", len(items))

    print("Truncating RAW tables...")
    truncate_raw_tables(engine)

    print("Loading RAW tables...")
    load_raw(engine, users, products, orders, items)

    print("Done ✅")


if __name__ == "__main__":
    main()